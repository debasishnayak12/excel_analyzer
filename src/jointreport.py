import pandas as pd
import uuid
import os


# Load the Excel files (Replace with actual file names)
# file1 = "C:/Debu/main_analyzer/excel_analyzer/report_1oct24_26jan25_aonehotel.xlsx"
# df1 = pd.read_excel(file1)

# # Load the second Excel file
# file2 = "C:/Debu/main_analyzer/excel_analyzer/docs/report/bookingcom_report_7566caddcb9e4a10a7856706da69dd0b_.xlsx"
# df2 = pd.read_excel(file2)

def jointreport(df1,df2):

    unique_id = uuid.uuid4().hex

    output_dir = "docs/Bookingcomreport"  # Change to your desired folder
    output_file = F"merged_output{unique_id}.xlsx"
    output_path = os.path.join(output_dir, output_file)

    os.makedirs(output_dir, exist_ok=True)


    # Create 4 empty rows
    empty_rows = pd.DataFrame([[""] * max(len(df1.columns), len(df2.columns))]).iloc[:4]

    # Identify "Total" row in both DataFrames
    total_row_df1 = df1[df1.iloc[:, 0].astype(str).str.contains("Total", case=False, na=False)]
    total_row_df2 = df2[df2.iloc[:, 0].astype(str).str.contains("Total", case=False, na=False)]

    # Ensure both total rows exist
    if not total_row_df1.empty and not total_row_df2.empty:
        # Extract relevant amounts using column names
        column_pay_to_hotel = "PayToHotel"  # Replace with exact column name from df1
        column_hotel_need_to_pay = "HotelNeedToPay"  # Replace with exact column name from df2

        total_pay_to_hotel = total_row_df1[column_pay_to_hotel].values[0]
        total_hotel_need_to_pay = total_row_df2[column_hotel_need_to_pay].values[0]
        print("total_pay_to_hotel",total_pay_to_hotel)
        print("total_hotel_need_to_pay",total_hotel_need_to_pay)

        if total_pay_to_hotel > total_hotel_need_to_pay:
            # Calculate final amount
            final_amount = total_pay_to_hotel - total_hotel_need_to_pay

            # Create DataFrame for "Final Amount Pay to Hotel" section
            df3 = pd.DataFrame({  
                "Final Amount Pay to Hotel": [final_amount]  
            })
            print("total_pay_to_hotel > total_hotel_need_to_pay")
        else:
            final_amount = total_hotel_need_to_pay - total_pay_to_hotel

            # Create DataFrame for "Final Amount Pay to Hotel" section
            df3 = pd.DataFrame({  
                "Final Amount Hotel Need To Pay": [final_amount]  
            })

            print("total_pay_to_hotel < total_hotel_need_to_pay")



        # Save to Excel with correct structure
        with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
            df1.to_excel(writer, index=False, startrow=0, header=True)  # First dataset with headers
            df2.to_excel(writer, index=False, startrow=len(df1) + 4, header=True)  # Second dataset with headers
            df3.to_excel(writer, index=False, startrow=len(df1) + len(df2) + 8, header=True)  # Final amount section

        print("Excel files merged successfully with both headers intact and final amount section added.")
        print("output_path",output_path)

        return output_path
