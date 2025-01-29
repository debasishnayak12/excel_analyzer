import numpy as np
import pandas as pd
import os
from pathlib import Path

import uuid

unique_id = uuid.uuid4().hex

def mmt_result(file1, file2):
    print("mmt function start")
    # Load the data
    _ ,ext = os.path.splitext(file1)
    if ext == '.xlsx':
        df_mmt = pd.read_excel(file1)
    else:
        df_mmt = pd.read_csv(file1)
    df_flexi= pd.read_excel(file2)
    df_flexi.rename(columns={
    'Booking Id': 'BookingID', 
    'Guest': 'Customer Name', 
    'Source': 'Booking Vendor', 
    'Check In Date': 'Check-in', 
    'Check Out Date': 'Check-out',
    'Payment Made (INR)': 'Hotel Gross Charges (A+B+C+T)'
    
    }, inplace=True)

    # Convert 'Booking Vendor' to lowercase for consistency
    df_flexi['Booking Vendor'] = df_flexi['Booking Vendor'].str.lower()

    # Filter second table where 'Payment Status' is 'Processed'
    df_mmt_filtered_processed = df_mmt[df_mmt['Payment Status'] == 'Processed']
    df_mmt_filtered_pending = df_mmt[df_mmt['Payment Status'] == 'Pending']

    # Ensure 'Booking Vendor' is in lowercase in the second dataset for matching
    # df_mmt_filtered['Booking Vendor'] = df_mmt_filtered['Booking Vendor'].str.lower()
    df_mmt_filtered_processed.loc[:, 'Booking Vendor'] = df_mmt_filtered_processed['Booking Vendor'].str.lower()
    # Perform an inner join based on 'Customer Name', 'Booking Vendor', 'Check-in', 'Check-out'
    merged_df = pd.merge(df_flexi, df_mmt_filtered_processed, 
                        on=['Customer Name', 'Booking Vendor','Check-in','Check-out','Hotel Gross Charges (A+B+C+T)'], 
                        how='inner')

    # Select important columns to save
    important_columns = [
        'Customer Name', 'Booking Vendor','Room Charges (A)','Amount Paid', 'Payment Status', 
        'Payment Date'
    ]

    # Filter only required columns if they exist
    final_df = merged_df[[col for col in important_columns if col in merged_df.columns]]

    # Save the processed data in the 'docs' folder
    os.makedirs('docs/pending', exist_ok=True)  # Ensure 'docs/pending' folder exists
    os.makedirs('docs/processed', exist_ok=True)  # Ensure 'docs/processed' folder exists
    os.makedirs('docs/finaldata', exist_ok=True)  # Ensure 'docs/finaldata' folder exists
    pending_df_path = os.path.join('docs/pending', f'pending_{unique_id}.xlsx')
    df_mmt_filtered_pending.to_excel(pending_df_path,index=False)

    processed_df_path = os.path.join('docs/processed', f'processed_{unique_id}.xlsx')
    df_mmt_filtered_processed.to_excel(processed_df_path,index=False)

    final_df_output_path = os.path.join('docs/finaldata', f'final_bookings{unique_id}.xlsx')
    final_df.to_excel(final_df_output_path, index=False)

    # Check if the file was saved successfully
    if os.path.exists(final_df_output_path):
        return final_df_output_path
    else:
        return None