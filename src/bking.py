import pandas as pd
import os
from pathlib import Path
import numpy as np

def stayflexiBookingcom(file,percent):
    # Load the data
    data = pd.read_excel(file)

    # Filter the data
    filtered_data = data[
        data['Source'].isin(['BOOKING.COM']) & 
        (data['Booking Status'].isin(['ON_HOLD','CONFIRMED','CHECKED OUT']))
    ]
    
    # filtered_data_cancelled = data[
    #     data['Source'].isin(['BOOKING.COM']) & 
    #     (data['Booking Status'] == 'CANCELLED')
    # ]
    
    # Convert date columns
    filtered_data.loc[:, 'Check In Date'] = pd.to_datetime(
        filtered_data['Check In Date'], format='%d/%m/%Y'
    ).dt.strftime('%Y-%m-%d')
    filtered_data.loc[:, 'Check Out Date'] = pd.to_datetime(
        filtered_data['Check Out Date'], format='%d/%m/%Y'
    ).dt.strftime('%Y-%m-%d')

    # Create the output directory if it doesn't exist
    os.makedirs('docs/bkingcomReport', exist_ok=True)
    output_path = Path('docs/bkingcomReport') / f'BOOKINGCOM_REPORT{Path(file).name}'
    print("output path",output_path)


    importantcolumns = ['Booking Id','Guest','Booking Date','Source','Check In Date','Check Out Date','Total Amount (INR)']

    importantdata = filtered_data[importantcolumns]
    new_importahntdata = importantdata.copy()
    new_importahntdata.fillna(0, inplace=True)
    print("importantdata",importantdata)
    new_importahntdata.rename(columns={'Booking Id':'BookingID','Guest':'Customer Name','Source':'Booking Vendor'},inplace=True)

    new_importahntdata['(12%)GST ON Total Amount'] = new_importahntdata['Total Amount (INR)']*0.12
    new_importahntdata['Tabtrips share'] = (new_importahntdata['Total Amount (INR)'] - new_importahntdata['(12%)GST ON Total Amount']) * (percent)
    new_importahntdata['(18%)GST ON Tabtripsshare'] = new_importahntdata['Tabtrips share'] * 0.18

    new_importahntdata[['Total Amount (INR)', 'Tabtrips share', '(18%)GST ON Tabtripsshare']] = (
    new_importahntdata[['Total Amount (INR)', 'Tabtrips share', '(18%)GST ON Tabtripsshare']]
    .apply(pd.to_numeric, errors='coerce')
    )
    new_importahntdata['HotelNeedToPay'] = new_importahntdata['(12%)GST ON Total Amount'] + new_importahntdata['Tabtrips share'] +new_importahntdata['(18%)GST ON Tabtripsshare']
    print("importantdata final",new_importahntdata)

    new_row = pd.Series({
        'BookingID': "Total",
        'Customer Name': np.nan,
        'Booking Date': np.nan,
        'Booking Vendor': np.nan,
        'Check In Date': np.nan,
        'Check Out Date': np.nan,
        'Total Amount (INR)': new_importahntdata['Total Amount (INR)'].sum() ,
        '(12%)GST ON Total Amount': new_importahntdata['(12%)GST ON Total Amount'].sum(), # Keep as a number, not a string
        'Tabtrips share': new_importahntdata['Tabtrips share'].sum(),
        '(18%)GST ON Tabtripsshare': new_importahntdata['(18%)GST ON Tabtripsshare'].sum(),
        'HotelNeedToPay': new_importahntdata['HotelNeedToPay'].sum()
    })

    new_df = new_row.to_frame().T
    print("new_df",new_df.shape)

    # Concatenate both DataFrames
    final_data = pd.concat([new_importahntdata, new_df], ignore_index=True)
    final_data.to_excel(output_path, index=False)
 
    # Check if the file was saved successfully
    if output_path.exists():
        return str(output_path)
    else:
        return None
    
def cancelled(file):
    data = pd.read_excel(file)

    # Filter the data
    filtered_data = data[
        data['Source'].isin(['BOOKING.COM']) & 
        (data['Booking Status'] == 'CANCELLED')
    ]
    
    # Convert date columns
    filtered_data.loc[:, 'Check In Date'] = pd.to_datetime(
        filtered_data['Check In Date'], format='%d/%m/%Y'
    ).dt.strftime('%Y-%m-%d')
    filtered_data.loc[:, 'Check Out Date'] = pd.to_datetime(
        filtered_data['Check Out Date'], format='%d/%m/%Y'
    ).dt.strftime('%Y-%m-%d')

    # Create the output directory if it doesn't exist
    os.makedirs('docs/bookingcom/cancelled', exist_ok=True)
    output_path = Path('docs/bookingcom/cancelled') / f'BOOKINGCOM_cancelled{Path(file).name}'

    importantcolumns = ['Booking Id','Guest','Booking Date','Source','Check In Date','Check Out Date','Total Amount (INR)']

    # importantdata = filtered_data[importantcolumns]
    # importantdata_new = importantdata.copy()

    # importantdata_new.rename(columns={'Booking Id':'BookingID','Guest':'Customer Name','Source':'Booking Vendor'},inplace=True)
    # new_row = {
    #             'BookingID': f"Total",  # or you can use None if you prefer
    #             'Customer Name': np.nan,
    #             'Booking Date': np.nan,
    #             'Booking Vendor': np.nan,
    #             'Check In Date': np.nan,
    #             'Check Out Date': np.nan,
    #             'Total Amount (INR)': importantdata_new['Total Amount (INR)'].sum()
    #         }
    
    # new_df = pd.DataFrame([new_row])
    # final_data = pd.concat([importantdata, new_df], ignore_index=True)
    importantdata = filtered_data[importantcolumns].copy()

# Rename columns
    importantdata.rename(columns={'Booking Id': 'BookingID', 'Guest': 'Customer Name', 'Source': 'Booking Vendor'}, inplace=True)

    # Create a new row with total sum
    new_row = pd.Series({
        'BookingID': "Total",
        'Customer Name': np.nan,
        'Booking Date': np.nan,
        'Booking Vendor': np.nan,
        'Check In Date': np.nan,
        'Check Out Date': np.nan,
        'Total Amount (INR)': importantdata['Total Amount (INR)'].sum()  # Keep as a number, not a string
    })

    # Convert the new_row to a DataFrame and ensure column order matches
    new_df = new_row.to_frame().T

    # Concatenate both DataFrames
    final_data = pd.concat([importantdata, new_df], ignore_index=True)
    print("final_data",final_data)

    # importantdata['(12%)GST ON Total Amount'] = importantdata['Total Amount (INR)']*0.12
    # importantdata['Tabtrips share'] = (importantdata['Total Amount (INR)'] - importantdata['(12%)GST ON Total Amount']) * (percent)
    # importantdata['(18%)GST ON Tabtripsshare'] = importantdata['Tabtrips share'] * 0.18
    # importantdata['HotelNeedToPay'] = importantdata['(12%)GST ON Total Amount'] + importantdata['Tabtrips share'] +importantdata['(18%)GST ON Tabtripsshare']

    final_data.to_excel(output_path, index=False)

    # Check if the file was saved successfully
    if output_path.exists():
        return str(output_path)
    else:
        return None
    
