"""
extended_migration_validator.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module defines a drop‑in migration validation tool that can be used
inside KNIME's Python Script (legacy) node to compare a legacy EDW table
with its corresponding table on GCP.  The implementation is intended to
be self‑contained: it does **not** require any hard coded column names
and works purely off of the structure of the two supplied pandas
DataFrames.  It produces multiple tables of results ranging from
high‑level row and schema checks through aggregate comparisons, time
windows, full row‑level reconciliation, partition statistics and
distributional tests.

The validator operates in seven stages.  Each stage returns one or more
pandas DataFrames which can be bound to KNIME outputs.  The stages are
listed below with the corresponding output index (1‑based):

  1. Summary (output_table_1)
     - Row counts, schema differences, data type comparisons and null
       counts for shared columns.  All values are converted to strings
       for KNIME compatibility.
  2. Grand Totals (output_table_2)
     - For every numeric measure present in both sources, compute the
       total sum in GCP and EDW along with the difference and a simple
       match/mismatch flag.  Columns are named descriptively (e.g.
       ``Measure``, ``GCP Sum``, ``EDW Sum``, ``Difference``, ``Status``).
  3. Time Windows (output_table_3)
     - Produce a long (“tidy”) table containing aggregates for each
       measure across several pre‑defined time windows: Daily, month‑to‑
       date (MTD), quarter‑to‑date (QTD), year‑to‑date (YTD) and a
       monthly breakdown across the full date range.  For each window
       and measure the report includes the period label, the sums from
       GCP and EDW, their difference and a match/mismatch flag.
  4. Reconciliation – mismatches only (output_table_4)
     - Perform a full outer join on a deterministic per‑row key to
       identify the following categories: rows that exist only in GCP,
       rows that exist only in EDW and rows where the dimension values
       align but one or more measures differ.  The output includes
       side‑by‑side values for all measures along with their
       differences and a ``mismatch_type`` descriptor.
  5. Annotated GCP (output_table_5)
     - Return the original GCP DataFrame with two additional columns:
       ``validation_status`` (one of Match, In GCP Only, In EDW Only or
       Value Mismatch) and ``mismatch_details`` which lists the exact
       measures and deltas for any mismatching row.  This output is
       useful for downstream filters or dashboards.
  6. Partition Checks (output_table_6)
     - Compute basic statistics by partition (default frequency is
       monthly).  For each period and measure the report includes the
       row count in each source, the counts' difference, the sums of
       measures and their differences.  This helps identify localised
       discrepancies that might not appear in the grand totals.
  7. Distribution Statistics (output_table_7)
     - For every numeric measure perform a set of descriptive and
       statistical comparisons: mean, median, standard deviation,
       variance, a Kolmogorov–Smirnov two sample test to assess if the
       full distributions match and a Population Stability Index (PSI)
       to detect drift.  Each statistic is accompanied by differences
       and status flags where sensible.  The PSI is computed using 10
       equally spaced bins across the combined range of the two
       datasets.

The module is intentionally verbose and well commented.  Users wishing
to extend or customise behaviour (for example by adjusting the time
window logic or statistical thresholds) should find the code easy to
read and modify.

Usage
-----
To use the validator in KNIME, import this module in your Python
Script (legacy) node and instantiate the ``ExtendedMigrationValidator``
with the two input tables (GCP first, EDW second).  Then call
``run_all()`` to obtain a tuple of DataFrames ready to assign to the
node's output ports.  For example:

    from extended_migration_validator import ExtendedMigrationValidator
    validator = ExtendedMigrationValidator(input_table_1, input_table_2)
    out1, out2, out3, out4, out5, out6, out7 = validator.run_all()

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import pandas as pd
import numpy as np
from typing import List, Optional, Tuple, Dict, Any
from dataclasses import dataclass, field

try:
    # SciPy is available in this environment; use it for statistical tests.
    from scipy.stats import ks_2samp, chisquare  # type: ignore
    _has_scipy = True
except ImportError:
    # Fallback if SciPy is unavailable (the KS test will be approximated later)
    _has_scipy = False


@dataclass
class ExtendedMigrationValidator:
    """A high performance, descriptive validator for EDW→GCP migrations.

    This class is parameterised by two DataFrames and optional
    configuration parameters controlling tolerance and partition frequency.
    Internally it discovers dimension, measure and date columns without
    any hardcoded names.  Results are gathered into a variety of
    DataFrames to aid analysis.
    """

    gcp_df: pd.DataFrame
    edw_df: pd.DataFrame
    atol: float = 1e-9
    rtol: float = 1e-9
    partition_freq: str = "M"
    psi_bins: int = 10
    date_col: Optional[str] = field(init=False, default=None)
    measure_cols: List[str] = field(init=False, default_factory=list)
    dimension_cols: List[str] = field(init=False, default_factory=list)
    key_col: str = field(init=False, default="__comparison_id__")

    def __post_init__(self) -> None:
        # Work on copies to avoid mutating the inputs
        self.gcp = self.gcp_df.copy().reset_index(drop=True)
        self.edw = self.edw_df.copy().reset_index(drop=True)

        # Normalise column names by stripping whitespace
        self.gcp.columns = [str(c).strip() for c in self.gcp.columns]
        self.edw.columns = [str(c).strip() for c in self.edw.columns]

        # Remove duplicate named columns (retain the first occurrence)
        self.gcp = self.gcp.loc[:, ~self.gcp.columns.duplicated()]
        self.edw = self.edw.loc[:, ~self.edw.columns.duplicated()]

        # Standardise dtypes and string values
        self._normalise_dtypes_and_strings(self.gcp)
        self._normalise_dtypes_and_strings(self.edw)

        # Discover roles (date, measures, dimensions)
        self._discover_roles()

        # Coerce types for numeric and dimension columns
        self._coerce_types(self.gcp)
        self._coerce_types(self.edw)

        # Build a deterministic comparison key for row matching
        self._build_comparison_ids(self.gcp)
        self._build_comparison_ids(self.edw)

        # Print summary to console for user visibility in KNIME
        print(f"[Validator] Using date column: {self.date_col}")
        print(f"[Validator] Discovered measures: {self.measure_cols}")
        print(f"[Validator] Discovered dimensions: {self.dimension_cols}")
        print(f"[Validator] GCP rows: {len(self.gcp)}, EDW rows: {len(self.edw)}")

    # ----------------------------------------------------------------------
    # Helper methods
    # ----------------------------------------------------------------------
    @staticmethod
    def _normalise_dtypes_and_strings(df: pd.DataFrame) -> None:
        """Convert category columns to object and strip whitespace in object columns."""
        # Convert 'category' dtype to 'object'
        cat_cols = df.select_dtypes(include="category").columns
        if len(cat_cols) > 0:
            df[cat_cols] = df[cat_cols].astype("object")
        # Strip whitespace in strings (object dtype)
        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].where(df[col].isna(), df[col].astype(str).str.strip())

    def _discover_roles(self) -> None:
        """Identify date, measure and dimension columns based on dtype and names."""
        def find_date_column(df: pd.DataFrame) -> Optional[str]:
            # Prefer columns already of datetime type
            datetime_cols = df.select_dtypes(include=["datetime64[ns]", "datetime64[ns, UTC]"]).columns.tolist()
            if datetime_cols:
                # Pick the datetime column with the most non-null entries
                return max(datetime_cols, key=lambda c: df[c].notna().sum())
            # Heuristic: look for names containing common date tokens
            candidates = [c for c in df.columns if any(token in c.lower() for token in ["date", "asof", "as_of", "dt", "day", "period"])]
            for col in candidates:
                try:
                    parsed = pd.to_datetime(df[col], errors="raise", infer_datetime_format=True, utc=False)
                    df[col] = parsed
                    return col
                except Exception:
                    continue
            return None

        # Detect date columns in both datasets
        gcp_date = find_date_column(self.gcp)
        edw_date = find_date_column(self.edw)
        # Align the name if both exist but differ
        if gcp_date and edw_date and gcp_date != edw_date:
            if gcp_date not in self.edw.columns:
                self.edw.rename(columns={edw_date: gcp_date}, inplace=True)
                self.date_col = gcp_date
            else:
                self.date_col = edw_date
        else:
            self.date_col = gcp_date or edw_date
        # Ensure date columns are timezone naive and dtype datetime
        if self.date_col:
            for df in (self.gcp, self.edw):
                if self.date_col in df.columns:
                    parsed = pd.to_datetime(df[self.date_col], errors="coerce")
                    try:
                        parsed = parsed.dt.tz_localize(None)
                    except Exception:
                        pass
                    df[self.date_col] = parsed

        # Identify measure columns: numeric columns common to both (exclude booleans)
        def numeric_columns(df: pd.DataFrame) -> List[str]:
            cols = df.select_dtypes(include=[np.number]).columns.tolist()
            return [c for c in cols if df[c].dtype != bool]
        gcp_measures = set(numeric_columns(self.gcp))
        edw_measures = set(numeric_columns(self.edw))
        self.measure_cols = sorted(gcp_measures.intersection(edw_measures))

        # Dimensions are shared columns minus measures; include date if present
        shared = sorted(set(self.gcp.columns).intersection(set(self.edw.columns)))
        dims = [c for c in shared if c not in self.measure_cols]
        if self.date_col and self.date_col in dims:
            # Put date first for readability
            self.dimension_cols = [self.date_col] + [c for c in dims if c != self.date_col]
        else:
            self.dimension_cols = dims
        # If no dimensions exist, synthesize a constant dimension
        if len(self.dimension_cols) == 0:
            for df in (self.gcp, self.edw):
                df["__no_dimension__"] = "ALL"
            self.dimension_cols = ["__no_dimension__"]

    def _coerce_types(self, df: pd.DataFrame) -> None:
        """Coerce measures to float64 and non-date dimensions to object."""
        for col in self.measure_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("float64")
        for col in self.dimension_cols:
            if col == self.date_col:
                continue
            df[col] = df[col].astype("object")

    def _build_comparison_ids(self, df: pd.DataFrame) -> None:
        """Construct a stable comparison ID for each row to align duplicates."""
        dims = self.dimension_cols

        def dimension_hash(sub_df: pd.DataFrame) -> pd.Series:
            parts: Optional[pd.Series] = None
            for c in dims:
                if c == self.date_col and pd.api.types.is_datetime64_any_dtype(sub_df[c]):
                    col_part = sub_df[c].dt.strftime("%Y-%m-%d").fillna("NaT")
                else:
                    col_part = sub_df[c].astype(str).fillna("NaN")
                parts = col_part if parts is None else parts.str.cat(col_part, sep="|")
            return parts

        def sequence_within_group(sub_df: pd.DataFrame) -> pd.Series:
            if not self.measure_cols:
                # If there are no numeric measures, assign sequence based on original order
                return sub_df.groupby(dims, dropna=False).cumcount()
            # Stable sort by dimensions then measures
            tmp = sub_df.copy()
            tmp["_row_order_"] = np.arange(len(tmp))
            sort_cols = dims + self.measure_cols + ["_row_order_"]
            tmp = tmp.sort_values(by=sort_cols, kind="mergesort")
            seq_sorted = tmp.groupby(dims, dropna=False).cumcount()
            seq = pd.Series(index=tmp.index, data=seq_sorted.values, dtype="int64")
            return seq.reindex(sub_df.index)

        df["__dimension_hash__"] = dimension_hash(df)
        df["__row_sequence__"] = sequence_within_group(df).astype("int64")
        df[self.key_col] = df["__dimension_hash__"].str.cat(df["__row_sequence__"].astype(str), sep="#")

    # ----------------------------------------------------------------------
    # Stage 1: Summary
    # ----------------------------------------------------------------------
    def run_summary(self) -> pd.DataFrame:
        """Generate a high‑level summary of row counts, schemas, dtypes and null counts."""
        gcp_cols = set(self.gcp.columns)
        edw_cols = set(self.edw.columns)
        shared_cols = sorted(gcp_cols & edw_cols)

        # Row count comparison
        row_section = pd.DataFrame({
            "Section": ["Row Counts"],
            "Metric": ["Number of Rows"],
            "GCP Value": [len(self.gcp)],
            "EDW Value": [len(self.edw)],
            "Difference": [len(self.gcp) - len(self.edw)]
        })

        # Columns present in one source but not the other
        schema_section = pd.DataFrame({
            "Section": ["Schema Differences", "Schema Differences"],
            "Metric": ["Columns Only in GCP", "Columns Only in EDW"],
            "GCP Value": [", ".join(sorted(gcp_cols - edw_cols)), ""],
            "EDW Value": ["", ", ".join(sorted(edw_cols - gcp_cols))],
            "Difference": ["", ""]
        })

        # Data type comparison for shared columns
        dtype_records: List[Dict[str, Any]] = []
        for col in shared_cols:
            dtype_records.append({
                "Section": "Data Type Comparison (Shared Columns)",
                "Metric": col,
                "GCP Value": str(self.gcp[col].dtype),
                "EDW Value": str(self.edw[col].dtype),
                "Difference": "Same" if self.gcp[col].dtype == self.edw[col].dtype else "Different"
            })
        dtype_section = pd.DataFrame(dtype_records) if dtype_records else pd.DataFrame(columns=["Section","Metric","GCP Value","EDW Value","Difference"])

        # Null count comparison for shared columns
        null_records: List[Dict[str, Any]] = []
        for col in shared_cols:
            g_nulls = int(self.gcp[col].isna().sum())
            e_nulls = int(self.edw[col].isna().sum())
            null_records.append({
                "Section": "Null Count Comparison (Shared Columns)",
                "Metric": col,
                "GCP Value": g_nulls,
                "EDW Value": e_nulls,
                "Difference": g_nulls - e_nulls
            })
        null_section = pd.DataFrame(null_records) if null_records else pd.DataFrame(columns=["Section","Metric","GCP Value","EDW Value","Difference"])

        # Concatenate sections in order and ensure all values are strings
        summary = pd.concat([row_section, schema_section, dtype_section, null_section], ignore_index=True)
        return summary.astype(str)

    # ----------------------------------------------------------------------
    # Stage 2: Grand Totals
    # ----------------------------------------------------------------------
    def run_grand_totals(self) -> pd.DataFrame:
        """Compute total sums of all numeric measures in both sources with differences and status."""
        columns = ["Measure", "GCP Sum", "EDW Sum", "Difference", "Status"]
        if not self.measure_cols:
            return pd.DataFrame(columns=columns)

        g_sums = self.gcp[self.measure_cols].sum(numeric_only=True)
        e_sums = self.edw[self.measure_cols].sum(numeric_only=True)
        data: List[Dict[str, Any]] = []
        for m in self.measure_cols:
            g_val = g_sums.get(m, np.nan)
            e_val = e_sums.get(m, np.nan)
            diff = g_val - e_val if (pd.notna(g_val) and pd.notna(e_val)) else (g_val - e_val)
            status = "Match" if np.isclose(g_val, e_val, equal_nan=True, atol=self.atol, rtol=self.rtol) else "Mismatch"
            data.append({
                "Measure": m,
                "GCP Sum": g_val,
                "EDW Sum": e_val,
                "Difference": diff,
                "Status": status
            })
        return pd.DataFrame(data, columns=columns)

    # ----------------------------------------------------------------------
    # Stage 3: Time Windows
    # ----------------------------------------------------------------------
    def run_time_windows(self) -> pd.DataFrame:
        """Generate sums across daily, MTD, QTD, YTD and monthly windows for each measure."""
        columns = ["Measure", "Window", "Period", "GCP Sum", "EDW Sum", "Difference", "Status"]
        if not self.measure_cols or not self.date_col:
            return pd.DataFrame(columns=columns)
        if self.date_col not in self.gcp.columns or self.date_col not in self.edw.columns:
            return pd.DataFrame(columns=columns)

        # Determine the latest (most recent) date across both tables
        latest_g = self.gcp[self.date_col].dropna().max()
        latest_e = self.edw[self.date_col].dropna().max()
        valid_dates = [d for d in [latest_g, latest_e] if pd.notna(d)]
        if not valid_dates:
            return pd.DataFrame(columns=columns)
        latest = max(valid_dates)

        # Helper functions for date ranges
        def month_start(date: pd.Timestamp) -> pd.Timestamp:
            return pd.Timestamp(date.year, date.month, 1)
        def quarter_start(date: pd.Timestamp) -> pd.Timestamp:
            month = date.month
            first_month = 3 * ((month - 1) // 3) + 1
            return pd.Timestamp(date.year, first_month, 1)
        def year_start(date: pd.Timestamp) -> pd.Timestamp:
            return pd.Timestamp(date.year, 1, 1)

        # Define windows for latest date
        windows = [
            ("Daily", latest.normalize(), latest.normalize(), latest.strftime("%Y-%m-%d")),
            ("Month to Date", month_start(latest), latest.normalize(), month_start(latest).strftime("%Y-%m")),
            ("Quarter to Date", quarter_start(latest), latest.normalize(), f"{quarter_start(latest).year}-Q{((latest.month-1)//3)+1}"),
            ("Year to Date", year_start(latest), latest.normalize(), str(year_start(latest).year))
        ]

        # Precompute monthly sums for all months in the union of both tables
        # The 'Period' label for monthly window is YYYY-MM
        gcp_monthly = (self.gcp
                       .assign(_period=self.gcp[self.date_col].dt.to_period("M").astype(str))
                       .groupby("_period", dropna=False)[self.measure_cols]
                       .sum(numeric_only=True))
        edw_monthly = (self.edw
                       .assign(_period=self.edw[self.date_col].dt.to_period("M").astype(str))
                       .groupby("_period", dropna=False)[self.measure_cols]
                       .sum(numeric_only=True))
        all_periods = sorted(set(gcp_monthly.index) | set(edw_monthly.index))

        result_rows: List[Dict[str, Any]] = []
        # Compute window sums for each pre‑defined window
        for window_name, start_date, end_date, label in windows:
            # Filter rows in each table for the time range and sum measures
            g_filtered = self.gcp.loc[(self.gcp[self.date_col] >= start_date) & (self.gcp[self.date_col] <= end_date), self.measure_cols]
            e_filtered = self.edw.loc[(self.edw[self.date_col] >= start_date) & (self.edw[self.date_col] <= end_date), self.measure_cols]
            g_sums = g_filtered.sum(numeric_only=True)
            e_sums = e_filtered.sum(numeric_only=True)
            for m in self.measure_cols:
                g_val = g_sums.get(m, np.nan)
                e_val = e_sums.get(m, np.nan)
                diff = g_val - e_val if (pd.notna(g_val) and pd.notna(e_val)) else (g_val - e_val)
                status = "Match" if np.isclose(g_val, e_val, equal_nan=True, atol=self.atol, rtol=self.rtol) else "Mismatch"
                result_rows.append({
                    "Measure": m,
                    "Window": window_name,
                    "Period": label,
                    "GCP Sum": g_val,
                    "EDW Sum": e_val,
                    "Difference": diff,
                    "Status": status
                })
        # Compute monthly sums for each measure across all months
        for period in all_periods:
            g_row = gcp_monthly.loc[period] if period in gcp_monthly.index else pd.Series(index=self.measure_cols, dtype="float64")
            e_row = edw_monthly.loc[period] if period in edw_monthly.index else pd.Series(index=self.measure_cols, dtype="float64")
            for m in self.measure_cols:
                g_val = g_row.get(m, np.nan)
                e_val = e_row.get(m, np.nan)
                diff = g_val - e_val if (pd.notna(g_val) and pd.notna(e_val)) else (g_val - e_val)
                status = "Match" if np.isclose(g_val, e_val, equal_nan=True, atol=self.atol, rtol=self.rtol) else "Mismatch"
                result_rows.append({
                    "Measure": m,
                    "Window": "Monthly",
                    "Period": period,
                    "GCP Sum": g_val,
                    "EDW Sum": e_val,
                    "Difference": diff,
                    "Status": status
                })
        return pd.DataFrame(result_rows, columns=columns)

    # ----------------------------------------------------------------------
    # Stage 4 & 5: Reconciliation and Annotated GCP
    # ----------------------------------------------------------------------
    def run_reconciliation(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Perform a full outer join on the comparison key and return mismatches and annotated GCP."""
        key = self.key_col
        # Rename measures to suffix with source for side‑by‑side comparison
        gcp_renamed = self.gcp.rename(columns={m: f"{m}__GCP" for m in self.measure_cols})
        edw_renamed = self.edw.rename(columns={m: f"{m}__EDW" for m in self.measure_cols})

        # Build lists of columns to merge.  Include dimension columns only from the GCP side to
        # avoid duplicate names; EDW dimension columns are dropped for the merge to prevent
        # collisions.  We suffix only numeric measures for each side.
        gcp_merge_cols: List[str] = [key] + [c for c in self.dimension_cols if c != key and c in gcp_renamed.columns]
        gcp_merge_cols += [f"{m}__GCP" for m in self.measure_cols]
        edw_merge_cols: List[str] = [key] + [f"{m}__EDW" for m in self.measure_cols]
        merged = pd.merge(
            gcp_renamed[gcp_merge_cols],
            edw_renamed[edw_merge_cols],
            on=key,
            how="outer",
            suffixes=("", "")
        )

        # Determine presence of key in each side
        gcp_keys = set(self.gcp[key])
        edw_keys = set(self.edw[key])
        in_gcp = merged[key].isin(gcp_keys)
        in_edw = merged[key].isin(edw_keys)

        # Determine value mismatches for each measure
        if self.measure_cols:
            mismatch_flags = []
            for m in self.measure_cols:
                col_g = f"{m}__GCP"
                col_e = f"{m}__EDW"
                # If missing columns (due to schema diffs), fill with NaN
                if col_g not in merged.columns:
                    merged[col_g] = np.nan
                if col_e not in merged.columns:
                    merged[col_e] = np.nan
                # np.isclose returns a numpy array; wrap it in a Series for alignment
                same_array = np.isclose(merged[col_g], merged[col_e], equal_nan=True, atol=self.atol, rtol=self.rtol)
                same_series = pd.Series(same_array, index=merged.index)
                mismatch_flags.append(~same_series.rename(m))
            any_value_mismatch = pd.concat(mismatch_flags, axis=1).any(axis=1)
        else:
            any_value_mismatch = pd.Series(False, index=merged.index)

        # Classify mismatch type
        mismatch_type = np.where(~in_edw & in_gcp, "In GCP Only",
                          np.where(~in_gcp & in_edw, "In EDW Only",
                                   np.where(any_value_mismatch, "Value Mismatch", "Match")))
        merged["mismatch_type"] = mismatch_type

        # Build mismatch-only report
        mismatch_df = merged.loc[merged["mismatch_type"] != "Match"].copy()
        # Pull in dimension columns (prefer unsuffixed if available) for context
        dimension_columns_in_merged = [c for c in self.dimension_cols if c != key and c in mismatch_df.columns]
        # Create difference columns
        for m in self.measure_cols:
            col_g = f"{m}__GCP"
            col_e = f"{m}__EDW"
            if col_g not in mismatch_df.columns:
                mismatch_df[col_g] = np.nan
            if col_e not in mismatch_df.columns:
                mismatch_df[col_e] = np.nan
            mismatch_df[f"{m}__Difference"] = mismatch_df[col_g] - mismatch_df[col_e]

        report_columns = [key, "mismatch_type"] + dimension_columns_in_merged
        report_columns += [f"{m}__GCP" for m in self.measure_cols] + [f"{m}__EDW" for m in self.measure_cols] + [f"{m}__Difference" for m in self.measure_cols]
        report_columns = [c for c in report_columns if c in mismatch_df.columns]
        mismatch_output = mismatch_df[report_columns].reset_index(drop=True)

        # Build annotated GCP output
        status_map = merged[[key, "mismatch_type"]].drop_duplicates()
        gcp_annotated = self.gcp.merge(status_map, on=key, how="left")
        gcp_annotated["validation_status"] = gcp_annotated["mismatch_type"].fillna("Match")

        # Construct mismatch_details where relevant
        if self.measure_cols:
            # Bring side‑by‑side values for building the details string
            side_values = merged[[key] + [f"{m}__GCP" for m in self.measure_cols] + [f"{m}__EDW" for m in self.measure_cols]]
            gcp_annotated = gcp_annotated.merge(side_values, on=key, how="left")
            def build_details(row: pd.Series) -> str:
                if row["validation_status"] != "Value Mismatch":
                    return ""
                parts: List[str] = []
                for m in self.measure_cols:
                    gv = row.get(f"{m}__GCP")
                    ev = row.get(f"{m}__EDW")
                    same = np.isclose(gv, ev, equal_nan=True, atol=self.atol, rtol=self.rtol)
                    if not bool(same):
                        delta = (gv - ev) if (pd.notna(gv) and pd.notna(ev)) else np.nan
                        parts.append(f"{m}={gv}|{ev} (Δ={delta})")
                return "; ".join(parts)
            gcp_annotated["mismatch_details"] = gcp_annotated.apply(build_details, axis=1)
            # Drop helper measure columns
            helper_cols = [f"{m}__GCP" for m in self.measure_cols] + [f"{m}__EDW" for m in self.measure_cols]
            gcp_annotated.drop(columns=[c for c in helper_cols if c in gcp_annotated.columns], inplace=True)
        # Drop mismatch_type from the final annotated output
        if "mismatch_type" in gcp_annotated.columns:
            gcp_annotated.drop(columns=["mismatch_type"], inplace=True)

        return mismatch_output, gcp_annotated

    # ----------------------------------------------------------------------
    # Stage 6: Partition Checks
    # ----------------------------------------------------------------------
    def run_partition_checks(self) -> pd.DataFrame:
        """Compute partition level statistics (row counts and sums) for each period."""
        columns = ["Period", "Measure", "GCP Row Count", "EDW Row Count", "Row Count Difference",
                   "GCP Sum", "EDW Sum", "Sum Difference", "Status"]
        if not self.measure_cols or not self.date_col:
            return pd.DataFrame(columns=columns)
        if self.date_col not in self.gcp.columns or self.date_col not in self.edw.columns:
            return pd.DataFrame(columns=columns)

        # Determine the period label using the specified frequency (e.g. monthly 'M')
        gcp_periods = self.gcp[self.date_col].dt.to_period(self.partition_freq).astype(str)
        edw_periods = self.edw[self.date_col].dt.to_period(self.partition_freq).astype(str)
        # Build DataFrames with period labels
        gcp_df = self.gcp.assign(_period=gcp_periods)
        edw_df = self.edw.assign(_period=edw_periods)
        # Group by period and compute row counts and measure sums
        gcp_grouped = gcp_df.groupby("_period").agg({**{self.date_col: "count"}, **{m: "sum" for m in self.measure_cols}})
        edw_grouped = edw_df.groupby("_period").agg({**{self.date_col: "count"}, **{m: "sum" for m in self.measure_cols}})
        # Rename the row count column
        gcp_grouped.rename(columns={self.date_col: "GCP Row Count"}, inplace=True)
        edw_grouped.rename(columns={self.date_col: "EDW Row Count"}, inplace=True)
        # Ensure all periods appear on both sides
        all_periods = sorted(set(gcp_grouped.index) | set(edw_grouped.index))
        rows: List[Dict[str, Any]] = []
        for period in all_periods:
            gcp_row = gcp_grouped.loc[period] if period in gcp_grouped.index else pd.Series(index=gcp_grouped.columns, dtype="float64")
            edw_row = edw_grouped.loc[period] if period in edw_grouped.index else pd.Series(index=edw_grouped.columns, dtype="float64")
            gcp_count = gcp_row.get("GCP Row Count", 0.0)
            edw_count = edw_row.get("EDW Row Count", 0.0)
            count_diff = gcp_count - edw_count
            for m in self.measure_cols:
                g_val = gcp_row.get(m, np.nan)
                e_val = edw_row.get(m, np.nan)
                sum_diff = g_val - e_val if (pd.notna(g_val) and pd.notna(e_val)) else (g_val - e_val)
                status = "Match" if (np.isclose(g_val, e_val, equal_nan=True, atol=self.atol, rtol=self.rtol) and np.isclose(gcp_count, edw_count, equal_nan=True, atol=self.atol, rtol=self.rtol)) else "Mismatch"
                rows.append({
                    "Period": period,
                    "Measure": m,
                    "GCP Row Count": gcp_count,
                    "EDW Row Count": edw_count,
                    "Row Count Difference": count_diff,
                    "GCP Sum": g_val,
                    "EDW Sum": e_val,
                    "Sum Difference": sum_diff,
                    "Status": status
                })
        return pd.DataFrame(rows, columns=columns)

    # ----------------------------------------------------------------------
    # Stage 7: Distribution Statistics
    # ----------------------------------------------------------------------
    def run_distribution_stats(self) -> pd.DataFrame:
        """Compute descriptive and distributional statistics for each numeric measure."""
        columns = ["Measure", "GCP Mean", "EDW Mean", "Mean Difference",
                   "GCP Median", "EDW Median", "Median Difference",
                   "GCP Std Dev", "EDW Std Dev", "Std Dev Difference",
                   "GCP Variance", "EDW Variance", "Variance Difference",
                   "KS Statistic", "KS p-value", "KS Pass", "PSI Value", "PSI Pass"]
        if not self.measure_cols:
            return pd.DataFrame(columns=columns)

        results: List[Dict[str, Any]] = []
        for m in self.measure_cols:
            g_series = self.gcp[m].dropna()
            e_series = self.edw[m].dropna()
            g_mean = g_series.mean()
            e_mean = e_series.mean()
            mean_diff = g_mean - e_mean
            g_median = g_series.median()
            e_median = e_series.median()
            median_diff = g_median - e_median
            g_std = g_series.std(ddof=0)
            e_std = e_series.std(ddof=0)
            std_diff = g_std - e_std
            g_var = g_series.var(ddof=0)
            e_var = e_series.var(ddof=0)
            var_diff = g_var - e_var
            # KS test (if available)
            if _has_scipy and len(g_series) > 0 and len(e_series) > 0:
                ks_stat, ks_p = ks_2samp(g_series, e_series)
            else:
                # Simple approximation: use quantile differences to derive a statistic (fall back)
                qs = np.linspace(0.0, 1.0, num=11)
                g_q = g_series.quantile(qs)
                e_q = e_series.quantile(qs)
                ks_stat = float(np.max(np.abs(g_q.values - e_q.values))) if (len(g_q) > 0 and len(e_q) > 0) else np.nan
                ks_p = np.nan
            ks_pass = ks_p >= 0.05 if not np.isnan(ks_p) else False
            # PSI calculation: use combined range and fixed number of bins
            psi_value = np.nan
            psi_pass = False
            if len(g_series) > 0 and len(e_series) > 0:
                # Use the combined min and max for bin edges
                combined_min = min(g_series.min(), e_series.min())
                combined_max = max(g_series.max(), e_series.max())
                # If min == max, bins collapse and PSI is zero
                if combined_min == combined_max:
                    psi_value = 0.0
                    psi_pass = True
                else:
                    bin_edges = np.linspace(combined_min, combined_max, self.psi_bins + 1)
                    g_counts, _ = np.histogram(g_series, bins=bin_edges)
                    e_counts, _ = np.histogram(e_series, bins=bin_edges)
                    g_ratios = g_counts / g_counts.sum() if g_counts.sum() > 0 else np.zeros_like(g_counts)
                    e_ratios = e_counts / e_counts.sum() if e_counts.sum() > 0 else np.zeros_like(e_counts)
                    # Replace zeros to avoid division by zero or log of zero
                    epsilon = 1e-12
                    g_ratios = np.where(g_ratios == 0, epsilon, g_ratios)
                    e_ratios = np.where(e_ratios == 0, epsilon, e_ratios)
                    psi_components = (g_ratios - e_ratios) * np.log(g_ratios / e_ratios)
                    psi_value = float(np.sum(psi_components))
                    psi_pass = psi_value < 0.1  # Threshold: <0.1 small difference

            results.append({
                "Measure": m,
                "GCP Mean": g_mean,
                "EDW Mean": e_mean,
                "Mean Difference": mean_diff,
                "GCP Median": g_median,
                "EDW Median": e_median,
                "Median Difference": median_diff,
                "GCP Std Dev": g_std,
                "EDW Std Dev": e_std,
                "Std Dev Difference": std_diff,
                "GCP Variance": g_var,
                "EDW Variance": e_var,
                "Variance Difference": var_diff,
                "KS Statistic": ks_stat,
                "KS p-value": ks_p,
                "KS Pass": ks_pass,
                "PSI Value": psi_value,
                "PSI Pass": psi_pass
            })
        return pd.DataFrame(results, columns=columns)

    # ----------------------------------------------------------------------
    # Orchestration
    # ----------------------------------------------------------------------
    def run_all(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Run all stages and return the seven output DataFrames."""
        summary_df = self.run_summary()
        grand_df = self.run_grand_totals()
        time_df = self.run_time_windows()
        mismatch_df, annotated_df = self.run_reconciliation()
        partition_df = self.run_partition_checks()
        distribution_df = self.run_distribution_stats()
        # Ensure summary is string typed for KNIME compatibility
        summary_df = summary_df.astype(str)
        return summary_df, grand_df, time_df, mismatch_df, annotated_df, partition_df, distribution_df