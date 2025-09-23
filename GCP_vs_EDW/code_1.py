# KNIME Python Script Node - Streamlined Migration Validator
# --------------------------------------------------------------------------
# This script validates a GCP data migration against an EDW (Teradata) source.
# It uses a staged approach for performance and clarity, producing four distinct
# output tables that detail validation results from high-level summaries to
# granular, row-level mismatches.

# INPUTS (provided automatically by KNIME):
#   - input_table_1: GCP DataFrame (the target system being validated)
#   - input_table_2: EDW/Teradata DataFrame (the source of truth)

# OUTPUTS (connect four output ports on the KNIME node):
#   - output_table_1: High-Level Summary (Row Counts, Schema, Nulls)
#   - output_table_2: Grand Total Comparison (Sum of all measures)
#   - output_table_3: GroupBy Dimension Comparison (Sum of measures by each dimension)
#   - output_table_4: Row-Level Mismatches (Detailed value differences on joined data)
# --------------------------------------------------------------------------

import pandas as pd
import numpy as np
import hashlib



class MigrationValidator:
    """
    Performs a staged, performance-optimized validation of a data migration
    from EDW (source) to GCP (target).
    """
    def __init__(self, gcp_df: pd.DataFrame, edw_df: pd.DataFrame):
        self.gcp_df = gcp_df.copy()
        self.edw_df = edw_df.copy()

        # --- Pre-computation for efficiency ---
        # Clean column names once
        self.gcp_df.columns = self.gcp_df.columns.str.strip()
        self.edw_df.columns = self.edw_df.columns.str.strip()

        # Identify common dimension and measure columns
        self.dimension_cols = sorted(
            list(
                set(self.gcp_df.select_dtypes(include=['object', 'category']).columns)
                .intersection(self.edw_df.select_dtypes(include=['object', 'category']).columns)
            )
        )
        if not self.dimension_cols:
            raise ValueError("No common dimension columns found for validation.")

        gcp_numeric = set(self.gcp_df.select_dtypes(include=np.number).columns)
        edw_numeric = set(self.edw_df.select_dtypes(include=np.number).columns)
        self.measure_cols = sorted(list(gcp_numeric.intersection(edw_numeric)))

        # Ensure measure columns are numeric before aggregation
        self.gcp_df[self.measure_cols] = self.gcp_df[self.measure_cols].apply(pd.to_numeric, errors='coerce')
        self.edw_df[self.measure_cols] = self.edw_df[self.measure_cols].apply(pd.to_numeric, errors='coerce')

        # Debugging: Print data types of measure columns
        print("GCP Measure Columns Data Types:")
        print(self.gcp_df[self.measure_cols].dtypes)
        print("EDW Measure Columns Data Types:")
        print(self.edw_df[self.measure_cols].dtypes)

        # Auto-detect the primary date column
        common_date_cols = set(self.gcp_df.columns).intersection(self.edw_df.columns)
        self.date_col = None
        for col in common_date_cols:
            if "DATE" in col.upper() or pd.api.types.is_datetime64_any_dtype(self.gcp_df[col]):
                self.date_col = col
                break

        # Update the date column reference after renaming
        if self.date_col:
            self.date_col_gcp = f"{self.date_col}_GCP"
            self.date_col_edw = f"{self.date_col}_EDW"
        else:
            self.date_col_gcp = None
            self.date_col_edw = None

        # Replace references to self.date_col with self.date_col_gcp and self.date_col_edw
        if self.date_col_gcp:
            self.gcp_df[self.date_col_gcp] = pd.to_datetime(self.gcp_df[self.date_col_gcp], errors='coerce')
        if self.date_col_edw:
            self.edw_df[self.date_col_edw] = pd.to_datetime(self.edw_df[self.date_col_edw], errors='coerce')

        # Generate unique row hashes for comparison
        self.id_col = '__comparison_id__'
        self.gcp_df[self.id_col] = self._generate_comparison_id(self.gcp_df)
        self.edw_df[self.id_col] = self._generate_comparison_id(self.edw_df)

        # Ensure no duplicate columns are added during processing
        self.gcp_df = self.gcp_df.loc[:, ~self.gcp_df.columns.duplicated()]
        self.edw_df = self.edw_df.loc[:, ~self.edw_df.columns.duplicated()]

        # Debugging: Log final column names after deduplication
        print("Final GCP Columns After Deduplication:", self.gcp_df.columns.tolist())
        print("Final EDW Columns After Deduplication:", self.edw_df.columns.tolist())

        # Ensure the DATE column is not duplicated during merging
        if self.date_col in self.gcp_df.columns and self.date_col in self.edw_df.columns:
            self.gcp_df = self.gcp_df.rename(columns={self.date_col: f"{self.date_col}_GCP"})
            self.edw_df = self.edw_df.rename(columns={self.date_col: f"{self.date_col}_EDW"})

    def _generate_comparison_id(self, df: pd.DataFrame) -> pd.Series:
        """
        Generate a unique hash ID for each row based on dimension columns.
        """
        if not self.dimension_cols:
            raise ValueError("Dimension columns must be identified before generating comparison IDs.")

        dim_data = df[self.dimension_cols].astype(str).apply(lambda x: '|'.join(x), axis=1)
        row_indices = df.index.astype(str)
        id_strings = dim_data + '|ROW_' + row_indices
        return id_strings.apply(lambda x: hashlib.md5(x.encode()).hexdigest())

    def _analyze_data_type_differences(self) -> pd.DataFrame:
        """
        Analyze data type differences between the two DataFrames.
        """
        differences = []
        common_cols = set(self.gcp_df.columns).intersection(set(self.edw_df.columns))

        for col in sorted(common_cols):
            gcp_dtype = str(self.gcp_df[col].dtype)
            edw_dtype = str(self.edw_df[col].dtype)
            if gcp_dtype != edw_dtype:
                differences.append({'Column': col, 'GCP_DType': gcp_dtype, 'EDW_DType': edw_dtype})

        return pd.DataFrame(differences)

    def run_summary_validation(self) -> pd.DataFrame:
        """
        Stage 1: Compares high-level metadata: row counts, column schemas,
        and summaries of null and unique values.
        """
        summary = []
        gcp_cols = set(self.gcp_df.columns)
        edw_cols = set(self.edw_df.columns)
        common_cols = gcp_cols.intersection(edw_cols)

        # 1. Row Count Comparison
        summary.append({'Check': 'Row Count', 'GCP': len(self.gcp_df), 'EDW': len(self.edw_df), 'Status': 'Match' if len(self.gcp_df) == len(self.edw_df) else 'Mismatch'})

        # 2. Column Name Comparison
        if gcp_cols == edw_cols:
            summary.append({'Check': 'Column Names', 'GCP': 'Match', 'EDW': 'Match', 'Status': 'Match'})
        else:
            gcp_only = ", ".join(gcp_cols - edw_cols)
            edw_only = ", ".join(edw_cols - gcp_cols)
            summary.append({'Check': 'Column Names (GCP Only)', 'GCP': gcp_only, 'EDW': '', 'Status': 'Mismatch'})
            summary.append({'Check': 'Column Names (EDW Only)', 'GCP': '', 'EDW': edw_only, 'Status': 'Mismatch'})

        # 3. Data Type, Nulls, and Unique Value Summaries
        for col in sorted(list(common_cols)):
            gcp_dtype = str(self.gcp_df[col].dtype)
            edw_dtype = str(self.edw_df[col].dtype)
            if gcp_dtype != edw_dtype:
                summary.append({'Check': f'DType: {col}', 'GCP': gcp_dtype, 'EDW': edw_dtype, 'Status': 'Mismatch'})

            gcp_nulls = self.gcp_df[col].isnull().sum()
            edw_nulls = self.edw_df[col].isnull().sum()
            if gcp_nulls != edw_nulls:
                summary.append({'Check': f'Null Count: {col}', 'GCP': gcp_nulls, 'EDW': edw_nulls, 'Status': 'Mismatch'})

        # Add data type differences to the summary
        dtype_differences = self._analyze_data_type_differences()
        if not dtype_differences.empty:
            for _, row in dtype_differences.iterrows():
                summary.append({'Check': f'DType Mismatch: {row["Column"]}', 'GCP': row["GCP_DType"], 'EDW': row["EDW_DType"], 'Status': 'Mismatch'})

        # Ensure no duplicate columns are added
        summary_df = pd.DataFrame(summary).astype(str)
        if 'DATE' in summary_df.columns:
            summary_df = summary_df.loc[:, ~summary_df.columns.duplicated()]

        return summary_df

    def run_grand_total_validation(self) -> pd.DataFrame:
        """
        Stage 2: Compares the grand sum of all common numeric columns (measures)
        across the entire dataset.
        """
        if not self.measure_cols:
            return pd.DataFrame({'Measure': ['No common numeric columns found.'], 'GCP_Sum': [0], 'EDW_Sum': [0], 'Difference': [0], 'Status': ['N/A']})

        gcp_totals = self.gcp_df[self.measure_cols].sum().rename('GCP_Sum')
        edw_totals = self.edw_df[self.measure_cols].sum().rename('EDW_Sum')

        report = pd.concat([gcp_totals, edw_totals], axis=1)
        report['Difference'] = report['GCP_Sum'] - report['EDW_Sum']
        report['Status'] = np.where(np.isclose(report['GCP_Sum'], report['EDW_Sum']), 'Match', 'Mismatch')

        return report.reset_index().rename(columns={'index': 'Measure'})

    def run_time_series_validation(self) -> pd.DataFrame:
        """
        Stage 3: Performs time-series validation by comparing aggregated measures
        over common time periods: Daily, MTD (Month-to-Date), QTD (Quarter-to-Date),
        and YTD (Year-to-Date).
        """
        if not self.date_col:
            return pd.DataFrame({'Message': ['No common date column found for time-series validation.']})

        # Adjust daily aggregation to use yesterday's data as "today"
        max_date = self.gcp_df[self.date_col].max()
        if pd.isnull(max_date):
            return pd.DataFrame({'Message': ['Invalid or missing dates in the GCP data.']})

        daily = max_date - pd.Timedelta(days=1)  # Yesterday's data
        mtd_start = max_date.replace(day=1)
        qtd_start = (max_date - pd.offsets.QuarterBegin(startingMonth=1)).normalize()
        ytd_start = max_date.replace(month=1, day=1)

        time_ranges = {
            'Daily': (daily, daily),
            'MTD': (mtd_start, daily),
            'QTD': (qtd_start, daily),
            'YTD': (ytd_start, daily)
        }

        results = []
        for measure in self.measure_cols:
            row = {'Measure': measure}
            for period, (start, end) in time_ranges.items():
                gcp_filtered = self.gcp_df[(self.gcp_df[self.date_col] >= start) & (self.gcp_df[self.date_col] <= end)]
                edw_filtered = self.edw_df[(self.edw_df[self.date_col] >= start) & (self.edw_df[self.date_col] <= end)]

                gcp_sum = gcp_filtered[measure].sum()
                edw_sum = edw_filtered[measure].sum()
                difference = gcp_sum - edw_sum
                status = 'Match' if np.isclose(gcp_sum, edw_sum) else 'Variance'

                row[f'{period}_Status'] = status
                row[f'{period}_Difference'] = difference
                row[f'{period}_GCP_Sum'] = gcp_sum
                row[f'{period}_EDW_Sum'] = edw_sum

            results.append(row)

        return pd.DataFrame(results)

    def _create_mismatch_details(self, merged: pd.DataFrame) -> pd.DataFrame:
        """
        Create detailed mismatch DataFrame with comprehensive status by comparison_id.
        """
        mismatches = []
        for measure in self.measure_cols:
            gcp_col, edw_col = f'{measure}_GCP', f'{measure}_EDW'
            mismatch_mask = ~np.isclose(merged[gcp_col], merged[edw_col], equal_nan=True)

            if mismatch_mask.any():
                mismatched_rows = merged.loc[mismatch_mask, self.dimension_cols + [gcp_col, edw_col]].copy()
                mismatched_rows['Measure'] = measure
                mismatches.append(mismatched_rows)

        if not mismatches:
            return pd.DataFrame({'Message': ['No mismatches found.']})

        return pd.concat(mismatches, ignore_index=True)

    def run_row_level_validation(self) -> pd.DataFrame:
        """
        Stage 4: Performs a row-level comparison by matching unique dimensions
        for each date, comparing the sum of each measure, and creating flags
        and descriptive columns for mismatches.
        """
        if not self.date_col:
            return pd.DataFrame({'Message': ['No common date column found for row-level validation.']})

        # Group by dimensions and date, then aggregate measures
        gcp_grouped = self.gcp_df.groupby(self.dimension_cols + [self.date_col])[self.measure_cols].sum().reset_index()
        edw_grouped = self.edw_df.groupby(self.dimension_cols + [self.date_col])[self.measure_cols].sum().reset_index()

        # Perform an outer join to include all rows from both datasets
        merged = pd.merge(gcp_grouped, edw_grouped, on=self.dimension_cols + [self.date_col], how='outer', suffixes=('_GCP', '_EDW'))

        # Initialize a list to store mismatch details
        mismatch_details = []

        for measure in self.measure_cols:
            gcp_col, edw_col = f'{measure}_GCP', f'{measure}_EDW'

            # Calculate differences and create flags
            merged[f'{measure}_Difference'] = merged[gcp_col] - merged[edw_col]
            merged[f'{measure}_Status'] = np.where(
                np.isclose(merged[gcp_col], merged[edw_col], equal_nan=True),
                'Match',
                'Mismatch'
            )

        # Add descriptive columns
        merged['Row_Status'] = np.where(
            merged[[f'{measure}_Status' for measure in self.measure_cols]].eq('Match').all(axis=1),
            'All Measures Match',
            'Some Measures Mismatch'
        )

        merged['Mismatch_Description'] = merged.apply(
            lambda row: ', '.join([
                f"{measure}: {row[f'{measure}_Difference']}"
                for measure in self.measure_cols
                if row[f'{measure}_Status'] == 'Mismatch'
            ]),
            axis=1
        )

        # Ensure consistent data types in dimension columns
        for col in self.dimension_cols + [self.date_col]:
            merged[col] = merged[col].astype(str)

        return merged

    def run_full_reconciliation(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Stage 4 & 5: Performs a full reconciliation by matching unique dimensions
        for each date, comparing the sum of each measure, and creating flags
        and descriptive columns for mismatches. Produces two outputs:
        - Full mismatch report (output_table_4)
        - GCP table with appended validation status (output_table_5)
        """
        if not self.date_col:
            return (
                pd.DataFrame({'Message': ['No common date column found for row-level validation.']})
                , self.gcp_df.assign(validation_status='No Date Column', mismatch_details='')
            )

        # Group by dimensions and date, then aggregate measures
        gcp_grouped = self.gcp_df.groupby(self.dimension_cols + [self.date_col])[self.measure_cols].sum().reset_index()
        edw_grouped = self.edw_df.groupby(self.dimension_cols + [self.date_col])[self.measure_cols].sum().reset_index()

        # Perform an outer join to include all rows from both datasets
        merged = pd.merge(
            gcp_grouped, edw_grouped,
            on=self.dimension_cols + [self.date_col],
            how='outer',
            suffixes=('_GCP', '_EDW')
        )

        # Initialize a list to store mismatch details
        mismatches = []

        for measure in self.measure_cols:
            gcp_col, edw_col = f'{measure}_GCP', f'{measure}_EDW'

            # Calculate differences and create flags
            merged[f'{measure}_Difference'] = merged[gcp_col] - merged[edw_col]
            merged[f'{measure}_Status'] = np.where(
                np.isclose(merged[gcp_col], merged[edw_col], equal_nan=True),
                'Match',
                'Mismatch'
            )

        # Add descriptive columns
        merged['Row_Status'] = np.where(
            merged[[f'{measure}_Status' for measure in self.measure_cols]].eq('Match').all(axis=1),
            'All Measures Match',
            'Some Measures Mismatch'
        )

        merged['Mismatch_Description'] = merged.apply(
            lambda row: ', '.join([
                f"{measure}: {row[f'{measure}_Difference']}"
                for measure in self.measure_cols
                if row[f'{measure}_Status'] == 'Mismatch'
            ]),
            axis=1
        )

        # Ensure consistent data types in dimension columns
        for col in self.dimension_cols + [self.date_col]:
            merged[col] = merged[col].astype(str)

        # Create the mismatch report (output_table_4)
        mismatch_report = merged[merged['Row_Status'] != 'All Measures Match']

        # Create the GCP table with appended validation status (output_table_5)
        gcp_with_status = self.gcp_df.copy()
        gcp_with_status = pd.merge(
            gcp_with_status,
            merged[[self.id_col, 'Row_Status', 'Mismatch_Description']],
            on=self.id_col,
            how='left'
        ).rename(columns={'Row_Status': 'validation_status', 'Mismatch_Description': 'mismatch_details'})

        return mismatch_report, gcp_with_status

# ==============================================================================
# KNIME EXECUTION LOGIC
# ==============================================================================

try:
    # KNIME-specific input handling
    # input_table_1 = knio.input_tables[0].to_pandas()
    # input_table_2 = knio.input_tables[1].to_pandas()

    # Initialize the validator with KNIME inputs
    validator = MigrationValidator(input_table_1, input_table_2) # type: ignore

    # --- Execute Each Validation Stage ---
    print("Stage 1: Running high-level summary validation...")
    output_table_1 = validator.run_summary_validation()

    print("Stage 2: Running grand total validation...")
    output_table_2 = validator.run_grand_total_validation()

    print("Stage 3: Running time-series validation...")
    output_table_3 = validator.run_time_series_validation()

    print("Stage 4 & 5: Running full reconciliation...")
    output_table_4, output_table_5 = validator.run_full_reconciliation()

    print("\nValidation complete. All output tables have been generated.")

except Exception as e:
    # Create error messages for all outputs if the script fails
    print(f"An error occurred during validation: {e}")
    error_df = pd.DataFrame({'Error': [str(e)]})
    output_table_1 = error_df.astype(str)
    output_table_2 = pd.DataFrame()
    output_table_3 = pd.DataFrame()
    output_table_4 = pd.DataFrame()
    output_table_5 = pd.DataFrame()