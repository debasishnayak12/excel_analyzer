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
    output_path = Path('docs/bookingcom') / f'BOOKINGCOM_REPORT{Path(file).name}'
    print("output path",output_path)

    # Save the filtered data to the specified path
    # filtered_data.to_excel(output_path, index=False)

    # Check if the file was saved successfully
    # if output_path.exists():
    #     return str(output_path)
    # else:
    #     return None

    importantcolumns = ['Booking Id','Guest','Booking Date','Source','Check In Date','Check Out Date','Total Amount (INR)','Payment Made (INR)']

    importantdata = filtered_data[importantcolumns]
    print("importantdata",importantdata)
    importantdata.rename(columns={'Booking Id':'BookingID','Guest':'Customer Name','Source':'Booking Vendor'},inplace=True)

    importantdata['(12%)GST ON Total Amount'] = importantdata['Total Amount (INR)']*0.12
    importantdata['Tabtrips share'] = (importantdata['Total Amount (INR)'] - importantdata['(12%)GST ON Total Amount']) * (percent)
    importantdata['(18%)GST ON Tabtripsshare'] = importantdata['Tabtrips share'] * 0.18
    importantdata['HotelNeedToPay'] = importantdata['(12%)GST ON Total Amount'] + importantdata['Tabtrips share'] +importantdata['(18%)GST ON Tabtripsshare']
    print("importantdata final",importantdata)
    importantdata.to_excel(output_path, index=False)
 
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

    # Save the filtered data to the specified path
    # filtered_data.to_excel(output_path, index=False)

    # Check if the file was saved successfully
    # if output_path.exists():
    #     return str(output_path)
    # else:
    #     return None

    importantcolumns = ['Booking Id','Guest','Booking Date','Source','Check In Date','Check Out Date','Total Amount (INR)']

    importantdata = filtered_data[importantcolumns]
    new_row = {
                'Booking Id': f"Total",  # or you can use None if you prefer
                'Guest': np.nan,
                'Booking Date': np.nan,
                'Source': np.nan,
                'Check In Date': np.nan,
                'Check Out Date': np.nan,
                'Total Amount (INR)': f"{importantdata['Total Amount (INR)']}"
            }
    
    new_df = pd.DataFrame([new_row])
    final_data = pd.concat([importantdata, new_df], ignore_index=True)

    final_data.rename(columns={'Booking Id':'BookingID','Guest':'Customer Name','Source':'Booking Vendor'},inplace=True)

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
    
