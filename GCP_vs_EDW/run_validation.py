import pandas as pd
from code_1 import MigrationValidator

# Load the CSV files
input_table_1 = pd.read_csv("GCP Data.CSV")
input_table_2 = pd.read_csv("EDW Data.CSV")

# Initialize the validator
validator = MigrationValidator(input_table_1, input_table_2)

# Execute each validation stage
print("Stage 1: Running high-level summary validation...")
output_table_1 = validator.run_summary_validation()
print(output_table_1)

print("\nStage 2: Running grand total validation...")
output_table_2 = validator.run_grand_total_validation()
print(output_table_2)

print("\nStage 3: Running GroupBy dimension validation...")
output_table_3 = validator.run_groupby_validation()
print(output_table_3)

print("\nStage 4: Running row-level validation...")
output_table_4 = validator.run_row_level_validation()
print(output_table_4)

print("\nValidation complete. All output tables have been generated.")
