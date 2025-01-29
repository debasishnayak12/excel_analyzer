import pandas as pd
import os
import uuid

uinque_id = uuid.uuid4().hex

# Load the two Excel files
# file1_path = "mmt_test.xlsx"  # Replace with your actual file path
# file2_path = "new_flexi_data.csv"  # Replace with your actual file path

def update_pending(file1,file2):
    _,ext1 = os.path.splitext(file1)
    _,ext2 = os.path.splitext(file2)

    if ext1 == '.xlsx':
        df1 = pd.read_excel(file1)  # First Excel file
    else:
        df1 = pd.read_csv(file1)  # First Excel file

    if ext2 == '.xlsx':
        df2 = pd.read_excel(file2)  # Second Excel file
    else:
        df2 = pd.read_csv(file2)  # Second Excel file

    # df1 = pd.read_excel(file1_path)  # First Excel file
    # df2 = pd.read_csv(file2_path)  # Second Excel file

    # Merge both files on 'Booking ID' to compare payment status
    merged_df = df1.merge(df2, on=['BookingID','Customer Name','Booking Vendor','Check-in','Check-out'], suffixes=('_old', '_new'))
    print("merged_df :",merged_df.columns)


    # Filter records where Payment Status changed from "Pending" to "Processed"
    filtered_df = merged_df[
        (merged_df['Payment Status_old'] == 'Pending') & 
        (merged_df['Payment Status_new'] == 'Processed')

    ]

    # Select necessary columns to export
    columns_to_keep = ['BookingID', 'Customer Name', 'Booking Vendor','Room Charges (A)_new','Amount Paid_new','Payment Status_new','Check-in','Check-out', 'Payment Date_new']

    result_df = filtered_df[columns_to_keep]

    result_df.rename(columns={
        'Room Charges (A)_new': 'Room Charges (A)',
        'Amount Paid_new': 'Amount Paid',
        'Payment Status_new': 'Payment Status',
        'Payment Date_new': 'Payment Date'
    })

    # Save the filtered data to a new Excel file
    output_path ="docs/pending"
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    output_file = os.path.join(output_path,f"docs/pending/new_pending{uinque_id}.xlsx")
    result_df.to_excel(output_file, index=False)
   
    if os.path.exists(output_file):
        return output_file
    else:
        return None