# KNIME Python Script (legacy) – GCP vs EDW Data Migration Validator
# Inputs:
#   input_table_1 -> GCP (BigQuery) data as pandas.DataFrame
#   input_table_2 -> EDW (Teradata/Legacy) data as pandas.DataFrame
# Outputs:
#   output_table_1 -> High-Level Summary (strings only)
#   output_table_2 -> Grand Total Comparison
#   output_table_3 -> Time-Based BI Report (Daily/MTD/QTD/YTD)
#   output_table_4 -> Full Reconciliation Mismatch Report (only mismatches)
#   output_table_5 -> GCP table with appended validation status and details

import pandas as pd
import numpy as np
from datetime import datetime
import math
import warnings

# Silence SettingWithCopy warnings (we’re already using .copy()/.loc)
warnings.simplefilter(action="ignore", category=pd.errors.SettingWithCopyWarning)

class MigrationValidator:
    """
    High-performance, plug-and-play migration validation.

    Design notes:
    - No hardcoded column names: dimensions/measures/date discovered at runtime.
    - Vectorized operations only (no iterrows).
    - Full outer-join reconciliation using a stable per-group sequence key to handle duplicates.
    - Five staged outputs per requirements.
    """

    def __init__(self, gcp_df: pd.DataFrame, edw_df: pd.DataFrame):
        # Work on copies to avoid KNIME view issues
        self.gcp = gcp_df.copy()
        self.edw = edw_df.copy()

        # Normalize column name casing/whitespace (non-destructive to values)
        self.gcp.columns = [str(c).strip() for c in self.gcp.columns]
        self.edw.columns = [str(c).strip() for c in self.edw.columns]

        # Harmonize dtypes for robust merging and arithmetic
        self._drop_dupe_columns()
        self._standardize_object_and_category()
        self._discover_roles()
        self._coerce_types()

        # Build stable comparison IDs for both sides
        self._build_comparison_ids()

    # ---------- Helpers: discovery & coercion ----------

    def _drop_dupe_columns(self):
        # KNIME sometimes passes duplicate-named columns if prior nodes appended; keep first occurrence
        self.gcp = self.gcp.loc[:, ~self.gcp.columns.duplicated()]
        self.edw = self.edw.loc[:, ~self.edw.columns.duplicated()]

    def _standardize_object_and_category(self):
        # Convert 'category' dtypes to object to avoid merge bugs
        for df in (self.gcp, self.edw):
            cat_cols = df.select_dtypes(include="category").columns
            if len(cat_cols) > 0:
                df[cat_cols] = df[cat_cols].astype("object")

        # Strip whitespace in object columns (string-like dims)
        for df in (self.gcp, self.edw):
            obj_cols = df.select_dtypes(include="object").columns
            for c in obj_cols:
                # Avoid exploding NaNs/non-strings; convert to string safely
                df[c] = df[c].where(df[c].isna(), df[c].astype(str).str.strip())

    def _discover_roles(self):
        """
        Discover:
          - date column (single): prefer datetime64 dtype; else guess by name and coerce
          - measure columns: numeric (float, int, boolean treated as numeric? -> no, keep bool as dimension)
          - dimension columns: all remaining
        """
        def pick_date_col(df: pd.DataFrame):
            # 1) True datetime columns
            dt_candidates = df.select_dtypes(include=["datetime64[ns]", "datetime64[ns, UTC]"]).columns.tolist()
            if dt_candidates:
                return dt_candidates[0]

            # 2) Name heuristics
            name_hits = [c for c in df.columns if any(k in c.lower() for k in ["date", "dt", "day", "asof", "period"])]
            # Try to parse each candidate quickly
            for c in name_hits:
                try:
                    parsed = pd.to_datetime(df[c], errors="raise", utc=False, infer_datetime_format=True)
                    df[c] = parsed
                    return c
                except Exception:
                    continue
            return None

        # Decide on a single canonical date column name used by both sides (if present in both)
        gcp_date = pick_date_col(self.gcp)
        edw_date = pick_date_col(self.edw)
        # Align name if both exist but names differ: rename EDW to GCP name where both are valid
        if gcp_date and edw_date and gcp_date != edw_date:
            # Only rename if no conflict
            if gcp_date not in self.edw.columns:
                self.edw.rename(columns={edw_date: gcp_date}, inplace=True)
                self.date_col = gcp_date
            else:
                self.date_col = edw_date
        else:
            self.date_col = gcp_date or edw_date  # whichever exists

        # Coerce the chosen date column on both
        if self.date_col:
            for df in (self.gcp, self.edw):
                if self.date_col in df.columns:
                    df[self.date_col] = pd.to_datetime(df[self.date_col], errors="coerce")

        # Measures: strictly numeric types (exclude bool)
        def numeric_cols(df):
            nums = df.select_dtypes(include=[np.number]).columns.tolist()
            # Exclude all-zero-width ints masquerading? (leave as-is)
            return [c for c in nums if df[c].dtype != bool]

        gcp_measures = set(numeric_cols(self.gcp))
        edw_measures = set(numeric_cols(self.edw))
        # Use intersection so we only compare columns present on both sides
        self.measure_cols = sorted(list(gcp_measures.intersection(edw_measures)))

        # Dimensions: shared columns minus measures
        shared_cols = sorted(list(set(self.gcp.columns).intersection(set(self.edw.columns))))
        self.dimension_cols = [c for c in shared_cols if c not in self.measure_cols]
        # Place date column (if any) into dimensions (it participates in grouping/time windows)
        if self.date_col and self.date_col not in self.dimension_cols and self.date_col in shared_cols:
            self.dimension_cols.append(self.date_col)

        # Keep a stable order: date first if present, then other dims
        if self.date_col and self.date_col in self.dimension_cols:
            self.dimension_cols = [self.date_col] + [c for c in self.dimension_cols if c != self.date_col]

    def _coerce_types(self):
        # Coerce measure columns to float64 for consistent math
        for df in (self.gcp, self.edw):
            for c in self.measure_cols:
                # If coercion fails, convert invalids to NaN
                df[c] = pd.to_numeric(df[c], errors="coerce").astype("float64")

        # Ensure dimension columns not in measures become object (except date)
        for df in (self.gcp, self.edw):
            for c in self.dimension_cols:
                if c == self.date_col:
                    continue
                if c in df.columns:
                    df[c] = df[c].astype("object")

    def _build_comparison_ids(self):
        """
        Create a stable per-row comparison ID:
          - Group by all discovered dimensions (excluding date? keep it in for exact day-level reconciliation)
          - Within each group, compute a deterministic sequence number using a stable sort on measures (asc)
          - comparison_id = hash(dim_values) + "#" + seq
        """
        dims_for_key = [c for c in self.dimension_cols]  # include date if present

        # If no dimension columns exist, synthesize a pseudo-dimension of constant value
        if not dims_for_key:
            const_col = "__no_dim__"
            for df in (self.gcp, self.edw):
                df[const_col] = "ALL"
            dims_for_key = [const_col]
            # reflect that in dimension cols for clarity
            if const_col not in self.dimension_cols:
                self.dimension_cols.append(const_col)

        def group_sequence(df: pd.DataFrame) -> pd.Series:
            if len(self.measure_cols) == 0:
                # If no measures, just assign cumcount on original order within dims group
                return df.groupby(dims_for_key).cumcount()

            # Build a stable sorting key across all measures (ascending)
            # Use fillna with a sentinel that won’t shuffle relative order unexpectedly (NaNs come last in sort_values)
            sort_cols = self.measure_cols
            sorted_df = df.copy()
            # Note: sort_values with list of columns works; kind='mergesort' is stable
            sorted_df["_tmp_sort_index_"] = np.arange(len(sorted_df))
            sorted_df = sorted_df.sort_values(by=dims_for_key + sort_cols + ["_tmp_sort_index_"], kind="mergesort")
            # Compute cumcount in sorted order, then restore original index alignment
            seq_sorted = sorted_df.groupby(dims_for_key).cumcount()
            seq = pd.Series(index=sorted_df.index, data=seq_sorted.values, dtype="int64")
            # Map back to original df order
            seq = seq.reindex(df.index)
            return seq

        def hash_dims(df: pd.DataFrame) -> pd.Series:
            # Build a single string key of dimension values (including date normalized as ISO)
            parts = []
            for c in dims_for_key:
                if c == self.date_col:
                    parts.append(df[c].dt.strftime("%Y-%m-%d").fillna("NaT") if pd.api.types.is_datetime64_any_dtype(df[c]) else df[c].astype(str))
                else:
                    parts.append(df[c].astype(str).fillna("NaN"))
            key = parts[0]
            for p in parts[1:]:
                key = key.str.cat(p, sep="|")
            return key

        for df, side in ((self.gcp, "GCP"), (self.edw, "EDW")):
            seq = group_sequence(df)
            base = hash_dims(df)
            df["__row_seq__"] = seq.astype("int64")
            df["__dim_hash__"] = base
            df["__comparison_id__"] = df["__dim_hash__"].str.cat(df["__row_seq__"].astype(str), sep="#")

        # For clarity in reconciliation
        self.key_col = "__comparison_id__"

    # ---------- Stage 1: High-Level Summary ----------

    def run_summary_validation(self) -> pd.DataFrame:
        # Row counts
        rc = pd.DataFrame({
            "Check": ["Row Count"],
            "GCP": [len(self.gcp)],
            "EDW": [len(self.edw)],
            "Difference": [len(self.gcp) - len(self.edw)]
        })

        # Column schemas (sets)
        gcp_cols = set(self.gcp.columns)
        edw_cols = set(self.edw.columns)
        schema = pd.DataFrame({
            "Check": ["Columns in GCP not in EDW", "Columns in EDW not in GCP"],
            "GCP": [", ".join(sorted(list(gcp_cols - edw_cols))), ""],
            "EDW": ["", ", ".join(sorted(list(edw_cols - gcp_cols)))],
            "Difference": ["", ""]
        })

        # Data types (shared columns)
        shared = sorted(list(gcp_cols.intersection(edw_cols)))
        dtypes_comp = []
        for c in shared:
            dtypes_comp.append({
                "Column": c,
                "GCP_dtype": str(self.gcp[c].dtype),
                "EDW_dtype": str(self.edw[c].dtype),
                "Same": str(self.gcp[c].dtype == self.edw[c].dtype)
            })
        dtypes_df = pd.DataFrame(dtypes_comp) if dtypes_comp else pd.DataFrame(columns=["Column","GCP_dtype","EDW_dtype","Same"])

        # Null counts for shared columns
        nulls_comp = []
        for c in shared:
            nulls_comp.append({
                "Column": c,
                "GCP_nulls": int(self.gcp[c].isna().sum()),
                "EDW_nulls": int(self.edw[c].isna().sum()),
                "Diff_nulls": int(self.gcp[c].isna().sum() - self.edw[c].isna().sum())
            })
        nulls_df = pd.DataFrame(nulls_comp) if nulls_comp else pd.DataFrame(columns=["Column","GCP_nulls","EDW_nulls","Diff_nulls"])

        # Make a vertically concatenated "report", and convert to strings for KNIME
        blocks = []

        rc["Section"] = "Row Count"
        schema["Section"] = "Schema"
        dtypes_df["Section"] = "DTypes (Shared)"
        nulls_df["Section"] = "Null Counts (Shared)"

        # Reorder columns for readability
        rc = rc[["Section","Check","GCP","EDW","Difference"]].astype(str)
        schema = schema[["Section","Check","GCP","EDW","Difference"]].astype(str)
        dtypes_df = dtypes_df[["Section","Column","GCP_dtype","EDW_dtype","Same"]].astype(str)
        nulls_df = nulls_df[["Section","Column","GCP_nulls","EDW_nulls","Diff_nulls"]].astype(str)

        blocks.extend([rc, schema, dtypes_df, nulls_df])
        out = pd.concat(blocks, ignore_index=True, sort=False).fillna("")
        return out.astype(str)

    # ---------- Stage 2: Grand Totals across measures ----------

    def run_grand_total_validation(self) -> pd.DataFrame:
        if not self.measure_cols:
            return pd.DataFrame(columns=["Measure","GCP_Sum","EDW_Sum","Difference","Status"])

        gcp_sums = self.gcp[self.measure_cols].sum(numeric_only=True)
        edw_sums = self.edw[self.measure_cols].sum(numeric_only=True)

        df = pd.DataFrame({
            "Measure": self.measure_cols,
            "GCP_Sum": [gcp_sums.get(m, np.nan) for m in self.measure_cols],
            "EDW_Sum": [edw_sums.get(m, np.nan) for m in self.measure_cols]
        })
        df["Difference"] = df["GCP_Sum"] - df["EDW_Sum"]
        df["Status"] = np.where(self._is_close(df["Difference"]), "Match", "Mismatch")
        return df

    # ---------- Stage 3: Time-based BI report ----------

    def run_time_series_validation(self) -> pd.DataFrame:
        cols = ["Measure",
                "Daily_Status","Daily_Difference",
                "MTD_Status","MTD_Difference",
                "QTD_Status","QTD_Difference",
                "YTD_Status","YTD_Difference"]
        if not self.measure_cols or (self.date_col is None) or (self.date_col not in self.gcp.columns) or (self.date_col not in self.edw.columns):
            # If missing date context, return empty with headers
            return pd.DataFrame(columns=cols)

        # Find the latest date across both sources (use union, ignore NaT)
        latest_gcp = self.gcp[self.date_col].dropna().max()
        latest_edw = self.edw[self.date_col].dropna().max()
        latest = max(latest_gcp, latest_edw) if pd.notna(latest_gcp) or pd.notna(latest_edw) else None
        if latest is None or pd.isna(latest):
            return pd.DataFrame(columns=cols)

        # Build ranges
        # Daily = latest date only
        def month_start(d): return pd.Timestamp(year=d.year, month=d.month, day=1)
        def quarter_start(d): return pd.Timestamp(year=d.year, month=(3*((d.month-1)//3)+1), day=1)
        def year_start(d): return pd.Timestamp(year=d.year, month=1, day=1)

        ranges = {
            "Daily": (latest.normalize(), latest.normalize()),
            "MTD":   (month_start(latest), latest.normalize()),
            "QTD":   (quarter_start(latest), latest.normalize()),
            "YTD":   (year_start(latest), latest.normalize())
        }

        # Pre-filter rows per window and aggregate vectorized
        def window_sum(df, start, end):
            mask = (df[self.date_col] >= start) & (df[self.date_col] <= end)
            return df.loc[mask, self.measure_cols].sum(numeric_only=True)

        rows = []
        for m in self.measure_cols:
            g_vals = {}
            e_vals = {}
            for label, (start, end) in ranges.items():
                g_vals[label] = window_sum(self.gcp, start, end).get(m, np.nan)
                e_vals[label] = window_sum(self.edw, start, end).get(m, np.nan)

            row = {
                "Measure": m,
                "Daily_Difference": g_vals["Daily"] - e_vals["Daily"],
                "MTD_Difference":   g_vals["MTD"]   - e_vals["MTD"],
                "QTD_Difference":   g_vals["QTD"]   - e_vals["QTD"],
                "YTD_Difference":   g_vals["YTD"]   - e_vals["YTD"],
            }
            row["Daily_Status"] = "Match" if self._is_close(row["Daily_Difference"]) else "Mismatch"
            row["MTD_Status"]   = "Match" if self._is_close(row["MTD_Difference"]) else "Mismatch"
            row["QTD_Status"]   = "Match" if self._is_close(row["QTD_Difference"]) else "Mismatch"
            row["YTD_Status"]   = "Match" if self._is_close(row["YTD_Difference"]) else "Mismatch"
            rows.append(row)

        out = pd.DataFrame(rows, columns=cols)
        return out

    # ---------- Stages 4 & 5: Full reconciliation and annotated GCP ----------

    def run_full_reconciliation(self):
        """
        Produces:
          - mismatches_only: rows where a comparison issue exists, with mismatch_type
          - gcp_with_status: original GCP rows + validation_status + mismatch_details
        """
        # Prepare left and right frames with renamed measure columns to avoid collisions
        left = self.gcp.copy()
        right = self.edw.copy()

        # Ensure key exists
        key = self.key_col

        # Suffix measure columns after merge to compare side-by-side
        gcp_meas = {m: f"{m}__GCP" for m in self.measure_cols}
        edw_meas = {m: f"{m}__EDW" for m in self.measure_cols}

        left_ren = left.rename(columns=gcp_meas)
        right_ren = right.rename(columns=edw_meas)

        # Drop category dtypes if any slipped back in
        for df in (left_ren, right_ren):
            cats = df.select_dtypes(include="category").columns
            if len(cats) > 0:
                df[cats] = df[cats].astype("object")

        # Full outer join on comparison key
        merged = pd.merge(
            left_ren[[key] + [c for c in left_ren.columns if c != key]],
            right_ren[[key] + [c for c in right_ren.columns if c != key]],
            on=key,
            how="outer",
            suffixes=("", "")
        )

        # Determine presence flags
        in_gcp = merged[[key]].merge(left[[key]], on=key, how="left", indicator=True)["_merge"].eq("both")
        in_edw = merged[[key]].merge(right[[key]], on=key, how="left", indicator=True)["_merge"].eq("both")

        # Compute value mismatches across measures
        # Build boolean DataFrame per-measure: True if values differ (NaN vs value counts as mismatch; NaN vs NaN = match)
        mism_bools = []
        for m in self.measure_cols:
            lg = f"{m}__GCP"
            rg = f"{m}__EDW"
            if lg not in merged.columns:  # measure missing on that side due to schema differences
                merged[lg] = np.nan
            if rg not in merged.columns:
                merged[rg] = np.nan

            left_vals = merged[lg]
            right_vals = merged[rg]

            both_nan = left_vals.isna() & right_vals.isna()
            diff = ~(np.isclose(left_vals, right_vals, equal_nan=True))  # equal_nan True treats NaN==NaN as equal
            # But we want NaN vs value to be mismatch; np.isclose handles that via equal_nan, so keep diff
            diff = diff & ~both_nan
            mism_bools.append(diff.rename(m))

        if mism_bools:
            any_value_mismatch = pd.concat(mism_bools, axis=1).any(axis=1)
        else:
            any_value_mismatch = pd.Series(False, index=merged.index)

        # Classify mismatch type
        mismatch_type = np.where(~in_edw & in_gcp, "In GCP Only",
                          np.where(~in_gcp & in_edw, "In EDW Only",
                                   np.where(any_value_mismatch, "Value Mismatch", "Match")))

        merged["mismatch_type"] = mismatch_type

        # Build mismatch-only report (Stage 4)
        mismatches_only = merged[merged["mismatch_type"] != "Match"].copy()

        # Include readable dimension context & diff details
        # Pull back dimension columns (prefer GCP side if available, else EDW side; because dims were not suffixed)
        dim_cols = [c for c in self.dimension_cols if c != self.key_col and c in merged.columns]
        # Compose details: list of measures where mismatched + numeric differences
        detail_cols = []
        for m in self.measure_cols:
            lg, rg = f"{m}__GCP", f"{m}__EDW"
            if lg not in mismatches_only.columns: mismatches_only[lg] = np.nan
            if rg not in mismatches_only.columns: mismatches_only[rg] = np.nan
            mismatches_only[f"{m}__Diff"] = mismatches_only[lg] - mismatches_only[rg]
            detail_cols.append(f"{m}__Diff")

        # Reorder columns for the report
        base_cols = [self.key_col, "mismatch_type"]
        report_cols = base_cols + dim_cols + \
                      [f"{m}__GCP" for m in self.measure_cols] + \
                      [f"{m}__EDW" for m in self.measure_cols] + \
                      [f"{m}__Diff" for m in self.measure_cols]
        # Keep only existing columns
        report_cols = [c for c in report_cols if c in mismatches_only.columns]
        mismatches_only = mismatches_only[report_cols].reset_index(drop=True)

        # Build GCP with validation status (Stage 5)
        # Map mismatch status back to each GCP row via key
        key_to_status = merged[[self.key_col, "mismatch_type"]].drop_duplicates()
        gcp_with_status = self.gcp.merge(key_to_status, on=self.key_col, how="left")
        gcp_with_status["validation_status"] = gcp_with_status["mismatch_type"].fillna("Match")

        # Build mismatch_details: comma-joined "col=GCP|EDW (Δ=...)" for mismatched measures in that row
        if self.measure_cols:
            # Join merged back to have side-by-side values for this row’s key
            key_to_values = merged[[self.key_col] +
                                   [f"{m}__GCP" for m in self.measure_cols] +
                                   [f"{m}__EDW" for m in self.measure_cols]]
            gcp_with_status = gcp_with_status.merge(key_to_values, on=self.key_col, how="left")

            def build_detail_row(row):
                if row.get("validation_status") != "Value Mismatch":
                    return ""
                parts = []
                for m in self.measure_cols:
                    g_val = row.get(f"{m}__GCP")
                    e_val = row.get(f"{m}__EDW")
                    # mismatch if not close (and not both NaN)
                    if not self._is_close_single(g_val, e_val):
                        diff = (g_val - e_val) if (pd.notna(g_val) and pd.notna(e_val)) else np.nan
                        parts.append(f"{m}={g_val}|{e_val} (Δ={diff})")
                return "; ".join(parts)

            # Vectorized via apply across row (only for GCP output, acceptable here)
            # Note: apply is row-wise but only for final annotation; core math above is vectorized
            gcp_with_status["mismatch_details"] = gcp_with_status.apply(build_detail_row, axis=1)

            # Drop helper columns from final annotated output for cleanliness
            drop_helpers = [f"{m}__GCP" for m in self.measure_cols] + [f"{m}__EDW" for m in self.measure_cols]
            gcp_with_status = gcp_with_status.drop(columns=[c for c in drop_helpers if c in gcp_with_status.columns])

        # Clean up
        if "mismatch_type" in gcp_with_status.columns:
            gcp_with_status = gcp_with_status.drop(columns=["mismatch_type"])

        return mismatches_only, gcp_with_status

    # ---------- Utilities ----------

    @staticmethod
    def _is_close(series_or_val, tol=1e-9):
        """
        Returns boolean Series (or scalar bool) indicating closeness to zero for differences.
        """
        if isinstance(series_or_val, pd.Series):
            return series_or_val.fillna(np.inf).abs() <= tol
        try:
            if pd.isna(series_or_val):
                return False
        except Exception:
            pass
        return abs(series_or_val) <= tol

    @staticmethod
    def _is_close_single(a, b, tol=1e-9):
        if pd.isna(a) and pd.isna(b):
            return True
        if pd.isna(a) or pd.isna(b):
            return False
        return abs(a - b) <= tol


# ===========================
# Main execution with safety
# ===========================
try:
    validator = MigrationValidator(input_table_1, input_table_2)

    # Stage 1
    output_table_1 = validator.run_summary_validation()

    # Stage 2
    output_table_2 = validator.run_grand_total_validation()

    # Stage 3
    output_table_3 = validator.run_time_series_validation()

    # Stages 4 & 5
    output_table_4, output_table_5 = validator.run_full_reconciliation()

    # Guarantee KNIME-friendly dtypes for output_table_1 (strings only)
    output_table_1 = output_table_1.astype(str)

except Exception as e:
    # Fail-safe: send error message to output_table_1; keep others empty but valid
    err_msg = pd.DataFrame({
        "Section": ["ERROR"],
        "Message": [str(e)],
        "Timestamp": [pd.Timestamp.utcnow().isoformat()]
    })
    output_table_1 = err_msg.astype(str)
    output_table_2 = pd.DataFrame(columns=["Measure","GCP_Sum","EDW_Sum","Difference","Status"])
    output_table_3 = pd.DataFrame(columns=[
        "Measure",
        "Daily_Status","Daily_Difference",
        "MTD_Status","MTD_Difference",
        "QTD_Status","QTD_Difference",
        "YTD_Status","YTD_Difference"
    ])
    output_table_4 = pd.DataFrame(columns=["__comparison_id__","mismatch_type"])
    output_table_5 = input_table_1.copy()
    output_table_5["validation_status"] = "ERROR"
    output_table_5["mismatch_details"] = str(e)
