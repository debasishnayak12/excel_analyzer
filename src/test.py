import pandas as pd
import numpy as np


# Load the first Excel file
file1 = "C:/Debu/main_analyzer/excel_analyzer/report_1oct24_26jan25_aonehotel.xlsx"
df1 = pd.read_excel(file1)

# Load the second Excel file
file2 = "C:/Debu/main_analyzer/excel_analyzer/docs/report/bookingcom_report_7566caddcb9e4a10a7856706da69dd0b_.xlsx"

df2 = pd.read_excel(file2)

# Remove header from first dataframe (keep structure)
# Create 4 empty rows (same number of columns as df1)
empty_rows = pd.DataFrame([[""] * df1.shape[1]], columns=df1.columns).iloc[:4]

# Concatenate first DataFrame, empty rows, and second DataFrame below
final_df = pd.concat([df1, empty_rows], ignore_index=True)

# Append the second dataframe below the first, keeping its headers
with pd.ExcelWriter("merged_output.xlsx", engine="xlsxwriter") as writer:
    final_df.to_excel(writer, index=False, startrow=0, header=True)  # First dataset with headers
    df2.to_excel(writer, index=False, startrow=len(final_df) + 1, header=True)  # Second dataset with headers

print("Excel files merged successfully with both headers intact!")