# KNIME Python Script (legacy) – EDW→GCP Migration Validator (Auto-Discovery, High-Performance)
# Inputs:
#   input_table_1 -> GCP (BigQuery) data as pandas.DataFrame
#   input_table_2 -> EDW (Teradata/Legacy) data as pandas.DataFrame
# Outputs:
#   output_table_1 -> High-Level Summary (strings only)
#   output_table_2 -> Grand Total Comparison for all measures
#   output_table_3 -> Time Windows + Monthly Breakdown (tidy format)
#   output_table_4 -> Full Reconciliation (mismatch-only) with mismatch_type
#   output_table_5 -> GCP table with appended validation_status & mismatch_details

import pandas as pd
import numpy as np
import warnings

# Quiet down chained-assignment warnings; we use .copy()/.loc deliberately
warnings.simplefilter("ignore", category=pd.errors.SettingWithCopyWarning)

class MigrationValidator:
    """
    Plug-and-play migration validator for KNIME.
    - Auto-discovers date, dimensions, and measures (no hardcoding).
    - Vectorized computations for speed (no iterrows loops for core logic).
    - Full outer-join reconciliation using a deterministic per-dimension-group sequence key.
    - Produces 5 outputs covering summary, totals, time windows (Daily/MTD/QTD/YTD + Monthly),
      mismatch-only details, and GCP rows annotated with validation status.
    """

    # Tunable numeric tolerance (abs + relative) for equality checks
    ATOL = 1e-9
    RTOL = 1e-9

    def __init__(self, gcp_df: pd.DataFrame, edw_df: pd.DataFrame):
        self.gcp = gcp_df.copy()
        self.edw = edw_df.copy()

        # Normalize column names (no case/space modifications beyond trim)
        self.gcp.columns = [str(c).strip() for c in self.gcp.columns]
        self.edw.columns = [str(c).strip() for c in self.edw.columns]

        self._remove_duplicate_named_columns()
        self._normalize_dtypes_and_strings()
        self._discover_roles()       # sets self.date_col, self.measure_cols, self.dimension_cols
        self._coerce_types()         # makes measures numeric, dims object (date stays datetime)
        self._build_comparison_ids() # creates self.key_col="__comparison_id__"

        # Helpful runtime log (visible in KNIME console)
        print("[Validator] Date column:", self.date_col)
        print("[Validator] Measures:", self.measure_cols)
        print("[Validator] Dimensions:", self.dimension_cols)
        print("[Validator] GCP rows:", len(self.gcp), "EDW rows:", len(self.edw))

    # ---------- Setup helpers ----------

    def _remove_duplicate_named_columns(self):
        self.gcp = self.gcp.loc[:, ~self.gcp.columns.duplicated()]
        self.edw = self.edw.loc[:, ~self.edw.columns.duplicated()]

    def _normalize_dtypes_and_strings(self):
        for df in (self.gcp, self.edw):
            # Convert category -> object to avoid merge/type edge cases
            cat_cols = df.select_dtypes(include="category").columns
            if len(cat_cols) > 0:
                df[cat_cols] = df[cat_cols].astype("object")
            # Strip whitespace in object columns
            for c in df.select_dtypes(include="object").columns:
                df[c] = df[c].where(df[c].isna(), df[c].astype(str).str.strip())

    def _discover_roles(self):
        def pick_date_col(df: pd.DataFrame):
            # 1) Prefer true datetimes
            dts = df.select_dtypes(include=["datetime64[ns]", "datetime64[ns, UTC]"]).columns.tolist()
            if dts:
                # If multiple, pick the one with most non-null values
                return max(dts, key=lambda c: df[c].notna().sum())

            # 2) Heuristic names then try parse
            name_hits = [c for c in df.columns
                         if any(k in c.lower() for k in ["date", "as_of", "asof", "dt", "day", "period"])]
            for c in name_hits:
                try:
                    parsed = pd.to_datetime(df[c], errors="raise", infer_datetime_format=True, utc=False)
                    df[c] = parsed
                    return c
                except Exception:
                    continue
            return None

        gcp_date = pick_date_col(self.gcp)
        edw_date = pick_date_col(self.edw)

        # Align the date column name across both if both exist but differ
        if gcp_date and edw_date and gcp_date != edw_date and gcp_date not in self.edw.columns:
            self.edw.rename(columns={edw_date: gcp_date}, inplace=True)
            self.date_col = gcp_date
        else:
            self.date_col = gcp_date or edw_date

        # Ensure datetime and strip timezone to naive for consistent comparisons
        if self.date_col:
            for df in (self.gcp, self.edw):
                if self.date_col in df.columns:
                    d = pd.to_datetime(df[self.date_col], errors="coerce")
                    try:
                        d = d.dt.tz_localize(None)
                    except Exception:
                        pass
                    df[self.date_col] = d

        # Measures = numeric intersection (exclude bools)
        def numeric_cols(df):
            cols = df.select_dtypes(include=[np.number]).columns.tolist()
            return [c for c in cols if df[c].dtype != bool]

        gcp_meas = set(numeric_cols(self.gcp))
        edw_meas = set(numeric_cols(self.edw))
        self.measure_cols = sorted(list(gcp_meas.intersection(edw_meas)))

        # Dimensions = shared columns minus measures; include date (if shared)
        shared = sorted(list(set(self.gcp.columns).intersection(set(self.edw.columns))))
        dims = [c for c in shared if c not in self.measure_cols]
        if self.date_col and self.date_col in shared and self.date_col not in dims:
            dims.append(self.date_col)

        # Put date first if present for readability
        if self.date_col and self.date_col in dims:
            self.dimension_cols = [self.date_col] + [c for c in dims if c != self.date_col]
        else:
            self.dimension_cols = dims

        # If no dimensions at all, synthesize one
        if len(self.dimension_cols) == 0:
            for df in (self.gcp, self.edw):
                df["__no_dim__"] = "ALL"
            self.dimension_cols = ["__no_dim__"]

    def _coerce_types(self):
        # Measures: numeric float64
        for df in (self.gcp, self.edw):
            for c in self.measure_cols:
                df[c] = pd.to_numeric(df[c], errors="coerce").astype("float64")
        # Dims: object (except date)
        for df in (self.gcp, self.edw):
            for c in self.dimension_cols:
                if c == self.date_col:
                    continue
                if c in df.columns:
                    df[c] = df[c].astype("object")

    def _build_comparison_ids(self):
        """
        Key strategy:
        - Build a dimension hash string (including date at day granularity if present).
        - Within each dimension group, assign a deterministic sequence number based on a stable
          sort by all measure columns. This pairs duplicate rows between systems deterministically.
        - comparison_id = "<dim_hash>#<seq>"
        """
        dims = list(self.dimension_cols)

        def dim_hash(df):
            parts = []
            for c in dims:
                if c == self.date_col and pd.api.types.is_datetime64_any_dtype(df[c]):
                    parts.append(df[c].dt.strftime("%Y-%m-%d").fillna("NaT"))
                else:
                    parts.append(df[c].astype(str).fillna("NaN"))
            key = parts[0]
            for p in parts[1:]:
                key = key.str.cat(p, sep="|")
            return key

        def seq_within_group(df):
            if len(self.measure_cols) == 0:
                return df.groupby(dims, dropna=False).cumcount()
            # Stable sort by dims + measures so both sides generate the same order
            tmp = df.copy()
            tmp["_tmp_idx_"] = np.arange(len(tmp))
            sort_cols = dims + self.measure_cols + ["_tmp_idx_"]
            tmp = tmp.sort_values(by=sort_cols, kind="mergesort")
            seq_sorted = tmp.groupby(dims, dropna=False).cumcount()
            seq = pd.Series(index=tmp.index, data=seq_sorted.values, dtype="int64")
            seq = seq.reindex(df.index)
            return seq

        for df in (self.gcp, self.edw):
            df["__dim_hash__"] = dim_hash(df)
            df["__row_seq__"]  = seq_within_group(df).astype("int64")
            df["__comparison_id__"] = df["__dim_hash__"].str.cat(df["__row_seq__"].astype(str), sep="#")

        self.key_col = "__comparison_id__"

    # ---------- Stage 1: Summary ----------

    def run_summary_validation(self) -> pd.DataFrame:
        gcp_cols = set(self.gcp.columns)
        edw_cols = set(self.edw.columns)
        shared   = sorted(list(gcp_cols & edw_cols))

        # Row count
        row_block = pd.DataFrame({
            "Section": ["Row Count"],
            "Check":   ["Rows"],
            "GCP":     [len(self.gcp)],
            "EDW":     [len(self.edw)],
            "Difference": [len(self.gcp) - len(self.edw)]
        })

        # Schema differences
        schema_block = pd.DataFrame({
            "Section": ["Schema","Schema"],
            "Check":   ["GCP_not_in_EDW","EDW_not_in_GCP"],
            "GCP":     [", ".join(sorted(gcp_cols - edw_cols)), ""],
            "EDW":     ["", ", ".join(sorted(edw_cols - gcp_cols))],
            "Difference": ["",""]
        })

        # Dtypes on shared columns
        dtype_rows = [{
            "Section":"DTypes (Shared)",
            "Column": c,
            "GCP_dtype": str(self.gcp[c].dtype),
            "EDW_dtype": str(self.edw[c].dtype),
            "Same": str(self.gcp[c].dtype == self.edw[c].dtype)
        } for c in shared]
        dtypes_block = pd.DataFrame(dtype_rows) if dtype_rows else pd.DataFrame(columns=["Section","Column","GCP_dtype","EDW_dtype","Same"])

        # Null counts on shared columns
        null_rows = [{
            "Section":"Null Counts (Shared)",
            "Column": c,
            "GCP_nulls": int(self.gcp[c].isna().sum()),
            "EDW_nulls": int(self.edw[c].isna().sum()),
            "Diff_nulls": int(self.gcp[c].isna().sum() - self.edw[c].isna().sum())
        } for c in shared]
        nulls_block = pd.DataFrame(null_rows) if null_rows else pd.DataFrame(columns=["Section","Column","GCP_nulls","EDW_nulls","Diff_nulls"])

        # Concatenate and force string type for KNIME serialization safety
        out = pd.concat([row_block, schema_block, dtypes_block, nulls_block], ignore_index=True).fillna("")
        return out.astype(str)

    # ---------- Stage 2: Grand Totals ----------

    def run_grand_total_validation(self) -> pd.DataFrame:
        cols = ["Measure","GCP_Sum","EDW_Sum","Difference","Status"]
        if not self.measure_cols:
            return pd.DataFrame(columns=cols)

        gsum = self.gcp[self.measure_cols].sum(numeric_only=True)
        esum = self.edw[self.measure_cols].sum(numeric_only=True)
        df = pd.DataFrame({
            "Measure": self.measure_cols,
            "GCP_Sum": [gsum.get(m, np.nan) for m in self.measure_cols],
            "EDW_Sum": [esum.get(m, np.nan) for m in self.measure_cols],
        })
        df["Difference"] = df["GCP_Sum"] - df["EDW_Sum"]
        df["Status"] = np.where(np.isclose(df["GCP_Sum"], df["EDW_Sum"], equal_nan=True,
                                           atol=self.ATOL, rtol=self.RTOL), "Match","Mismatch")
        return df

    # ---------- Stage 3: Time Windows (Daily/MTD/QTD/YTD + Monthly) ----------

    def run_time_windows_validation(self) -> pd.DataFrame:
        """
        Returns a tidy (long) DataFrame with:
          Measure, Window (Daily|MTD|QTD|YTD|Monthly), Period, GCP_Sum, EDW_Sum, Difference, Status
        - Daily period = latest date (YYYY-MM-DD)
        - MTD = latest month to date (Period=YYYY-MM)
        - QTD = latest quarter to date (Period=YYYY-Q#)
        - YTD = year to date (Period=YYYY)
        - Monthly = per-calendar-month across all available data (Period=YYYY-MM)
        """
        cols = ["Measure","Window","Period","GCP_Sum","EDW_Sum","Difference","Status"]
        if not self.measure_cols or not self.date_col:
            return pd.DataFrame(columns=cols)

        # If either side lacks date column, cannot compute windows
        if self.date_col not in self.gcp.columns or self.date_col not in self.edw.columns:
            return pd.DataFrame(columns=cols)

        # Determine latest date across both sides
        latest_g = self.gcp[self.date_col].dropna().max()
        latest_e = self.edw[self.date_col].dropna().max()
        latest = max(d for d in [latest_g, latest_e] if pd.notna(d)) if (pd.notna(latest_g) or pd.notna(latest_e)) else None
        if latest is None or pd.isna(latest):
            return pd.DataFrame(columns=cols)

        def month_start(d): return pd.Timestamp(d.year, d.month, 1)
        def quarter_first_month(m): return 3 * ((m - 1) // 3) + 1
        def quarter_start(d): return pd.Timestamp(d.year, quarter_first_month(d.month), 1)
        def year_start(d): return pd.Timestamp(d.year, 1, 1)

        daily_start = latest.normalize()
        daily_end   = latest.normalize()
        mtd_start   = month_start(latest)
        qtd_start   = quarter_start(latest)
        ytd_start   = year_start(latest)

        def window_sum(df, start, end):
            mask = (df[self.date_col] >= start) & (df[self.date_col] <= end)
            return df.loc[mask, self.measure_cols].sum(numeric_only=True)

        rows = []

        # Daily / MTD / QTD / YTD snapshots (at latest date)
        ranges = [
            ("Daily", daily_start, daily_end, daily_start.strftime("%Y-%m-%d")),
            ("MTD",   mtd_start,   daily_end, mtd_start.strftime("%Y-%m")),
            ("QTD",   qtd_start,   daily_end, f"{qtd_start.year}-Q{((latest.month-1)//3)+1}"),
            ("YTD",   ytd_start,   daily_end, str(ytd_start.year)),
        ]
        for window, start, end, label in ranges:
            g_agg = window_sum(self.gcp, start, end)
            e_agg = window_sum(self.edw, start, end)
            for m in self.measure_cols:
                gv = g_agg.get(m, np.nan)
                ev = e_agg.get(m, np.nan)
                diff = gv - ev if (pd.notna(gv) and pd.notna(ev)) else (gv - ev)
                status = "Match" if np.isclose(gv, ev, equal_nan=True, atol=self.ATOL, rtol=self.RTOL) else "Mismatch"
                rows.append({"Measure": m, "Window": window, "Period": label,
                             "GCP_Sum": gv, "EDW_Sum": ev, "Difference": diff, "Status": status})

        # Monthly breakdown across all available months in union of both tables
        def month_series(df):
            return df[self.date_col].dt.to_period("M").astype(str)

        gcp_month = self.gcp[[self.date_col]].dropna().assign(_month=lambda d: d[self.date_col].dt.to_period("M").astype(str))["_month"]
        edw_month = self.edw[[self.date_col]].dropna().assign(_month=lambda d: d[self.date_col].dt.to_period("M").astype(str))["_month"]
        all_months = sorted(set(gcp_month.unique()).union(set(edw_month.unique())))

        if all_months:
            # Pre-compute per-month sums for each source
            gcp_by_m = (self.gcp
                        .assign(_month=self.gcp[self.date_col].dt.to_period("M").astype(str))
                        .groupby("_month", dropna=False)[self.measure_cols]
                        .sum(numeric_only=True))
            edw_by_m = (self.edw
                        .assign(_month=self.edw[self.date_col].dt.to_period("M").astype(str))
                        .groupby("_month", dropna=False)[self.measure_cols]
                        .sum(numeric_only=True))
            # Emit rows per month
            for mo in all_months:
                g_row = gcp_by_m.loc[mo] if mo in gcp_by_m.index else pd.Series(index=self.measure_cols, dtype="float64")
                e_row = edw_by_m.loc[mo] if mo in edw_by_m.index else pd.Series(index=self.measure_cols, dtype="float64")
                for m in self.measure_cols:
                    gv = g_row.get(m, np.nan)
                    ev = e_row.get(m, np.nan)
                    diff = gv - ev if (pd.notna(gv) and pd.notna(ev)) else (gv - ev)
                    status = "Match" if np.isclose(gv, ev, equal_nan=True, atol=self.ATOL, rtol=self.RTOL) else "Mismatch"
                    rows.append({"Measure": m, "Window": "Monthly", "Period": mo,
                                 "GCP_Sum": gv, "EDW_Sum": ev, "Difference": diff, "Status": status})

        return pd.DataFrame(rows, columns=cols)

    # ---------- Stages 4 & 5: Full reconciliation + annotated GCP ----------

    def run_full_reconciliation(self):
        key = self.key_col

        # Prepare left/right with suffixed measure columns so we can compare side-by-side
        left = self.gcp.copy()
        right = self.edw.copy()
        left = left.rename(columns={m: f"{m}__GCP" for m in self.measure_cols})
        right = right.rename(columns={m: f"{m}__EDW" for m in self.measure_cols})

        # Ensure no lingering 'category' cols
        for df in (left, right):
            cats = df.select_dtypes(include="category").columns
            if len(cats) > 0:
                df[cats] = df[cats].astype("object")

        merged = pd.merge(
            left[[key] + [c for c in left.columns if c != key]],
            right[[key] + [c for c in right.columns if c != key]],
            on=key, how="outer", suffixes=("","")
        )

        # Presence flags via key membership
        gcp_keys = set(self.gcp[key].unique())
        edw_keys = set(self.edw[key].unique())
        in_gcp = merged[key].isin(gcp_keys)
        in_edw = merged[key].isin(edw_keys)

        # Value mismatches across measures
        if self.measure_cols:
            diffs = []
            for m in self.measure_cols:
                lg, rg = f"{m}__GCP", f"{m}__EDW"
                if lg not in merged.columns: merged[lg] = np.nan
                if rg not in merged.columns: merged[rg] = np.nan
                # np.isclose handles NaNs with equal_nan=True
                same = np.isclose(merged[lg], merged[rg], equal_nan=True, atol=self.ATOL, rtol=self.RTOL)
                diffs.append(~same.rename(m))
            any_value_mismatch = pd.concat(diffs, axis=1).any(axis=1) if diffs else pd.Series(False, index=merged.index)
        else:
            any_value_mismatch = pd.Series(False, index=merged.index)

        merged["mismatch_type"] = np.where(~in_edw & in_gcp, "In GCP Only",
                                    np.where(~in_gcp & in_edw, "In EDW Only",
                                             np.where(any_value_mismatch, "Value Mismatch", "Match")))

        # ---- Output 4: mismatch-only report
        mismatches_only = merged.loc[merged["mismatch_type"] != "Match"].copy()

        # Enrich with dimension context (prefer unsuffixed columns that survived merge)
        dim_cols = [c for c in self.dimension_cols if c != key and c in mismatches_only.columns]

        # Add per-measure diffs (GCP-EDW) to mismatch report
        for m in self.measure_cols:
            lg, rg = f"{m}__GCP", f"{m}__EDW"
            if lg not in mismatches_only.columns: mismatches_only[lg] = np.nan
            if rg not in mismatches_only.columns: mismatches_only[rg] = np.nan
            mismatches_only[f"{m}__Diff"] = mismatches_only[lg] - mismatches_only[rg]

        base_cols = [key, "mismatch_type"]
        report_cols = base_cols + dim_cols + \
                      [f"{m}__GCP" for m in self.measure_cols] + \
                      [f"{m}__EDW" for m in self.measure_cols] + \
                      [f"{m}__Diff" for m in self.measure_cols]
        report_cols = [c for c in report_cols if c in mismatches_only.columns]
        mismatches_only = mismatches_only[report_cols].reset_index(drop=True)

        # ---- Output 5: GCP with validation_status + mismatch_details
        status_map = merged[[key, "mismatch_type"]].drop_duplicates()
        gcp_with_status = self.gcp.merge(status_map, on=key, how="left")
        gcp_with_status["validation_status"] = gcp_with_status["mismatch_type"].fillna("Match")

        if self.measure_cols:
            # Bring side-by-side values for detail text
            side_vals = merged[[key] +
                               [f"{m}__GCP" for m in self.measure_cols] +
                               [f"{m}__EDW" for m in self.measure_cols]]
            gcp_with_status = gcp_with_status.merge(side_vals, on=key, how="left")

            def build_details(row):
                if row["validation_status"] != "Value Mismatch":
                    return ""
                parts = []
                for m in self.measure_cols:
                    gv = row.get(f"{m}__GCP")
                    ev = row.get(f"{m}__EDW")
                    # flag only those not close
                    same = np.isclose(gv, ev, equal_nan=True, atol=self.ATOL, rtol=self.RTOL)
                    if not bool(same):
                        delta = (gv - ev) if (pd.notna(gv) and pd.notna(ev)) else np.nan
                        parts.append(f"{m}={gv}|{ev} (Δ={delta})")
                return "; ".join(parts)

            # Row-wise apply only for final annotation string (acceptable)
            gcp_with_status["mismatch_details"] = gcp_with_status.apply(build_details, axis=1)

            drop_helpers = [f"{m}__GCP" for m in self.measure_cols] + [f"{m}__EDW" for m in self.measure_cols]
            gcp_with_status = gcp_with_status.drop(columns=[c for c in drop_helpers if c in gcp_with_status.columns])

        if "mismatch_type" in gcp_with_status.columns:
            gcp_with_status = gcp_with_status.drop(columns=["mismatch_type"])

        return mismatches_only, gcp_with_status

    # ---------- Orchestration ----------

    def run_all(self):
        out1 = self.run_summary_validation()
        out2 = self.run_grand_total_validation()
        out3 = self.run_time_windows_validation()
        out4, out5 = self.run_full_reconciliation()
        # Ensure KNIME-safe (strings) for summary table
        out1 = out1.astype(str)
        return out1, out2, out3, out4, out5


# ===========================
# Main (safe) execution
# ===========================
try:
    validator = MigrationValidator(input_table_1, input_table_2)
    output_table_1, output_table_2, output_table_3, output_table_4, output_table_5 = validator.run_all()

except Exception as e:
    # Fail safe: put error in output_table_1; keep other outputs valid but empty
    err = pd.DataFrame({
        "Section": ["ERROR"],
        "Message": [str(e)],
        "Timestamp": [pd.Timestamp.utcnow().isoformat()]
    }).astype(str)

    output_table_1 = err
    output_table_2 = pd.DataFrame(columns=["Measure","GCP_Sum","EDW_Sum","Difference","Status"])
    output_table_3 = pd.DataFrame(columns=["Measure","Window","Period","GCP_Sum","EDW_Sum","Difference","Status"])
    output_table_4 = pd.DataFrame(columns=["__comparison_id__","mismatch_type"])
    output_table_5 = input_table_1.copy()
    output_table_5["validation_status"] = "ERROR"
    output_table_5["mismatch_details"] = str(e)
