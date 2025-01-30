import pandas as pd
import os
from pathlib import Path

def stayflexiBookingcom(file):
    # Load the data
    data = pd.read_excel(file)

    # Filter the data
    filtered_data = data[
        data['Source'].isin(['BOOKING.COM']) & 
        (data['Booking Status'].isin(['ON_HOLD','CONFIRMED']))
    ]
    
    # Convert date columns
    filtered_data.loc[:, 'Check In Date'] = pd.to_datetime(
        filtered_data['Check In Date'], format='%d/%m/%Y'
    ).dt.strftime('%Y-%m-%d')
    filtered_data.loc[:, 'Check Out Date'] = pd.to_datetime(
        filtered_data['Check Out Date'], format='%d/%m/%Y'
    ).dt.strftime('%Y-%m-%d')

    # Create the output directory if it doesn't exist
    os.makedirs('docs/bookingcom', exist_ok=True)
    output_path = Path('docs/bookingcom') / f'confirmed_BOOKINGCOM_{Path(file).name}'

    # Save the filtered data to the specified path
    filtered_data.to_excel(output_path, index=False)

    # Check if the file was saved successfully
    # if output_path.exists():
    #     return str(output_path)
    # else:
    #     return None

    importantcolumns = ['Booking Id','Guest','Booking Date','Source','Booking Status','Check In Date','Check Out Date','Total Amount (INR)','Payment Made (INR)']

    importantdata = filtered_data[importantcolumns]

    importantdata.rename(columns={'Booking Id':'BookingID','Guest':'Customer Name','Source':'Booking Vendor'},inplace=True)

    importantdata['(12%)GST ON Total Amount'] = importantdata['Total Amount (INR)']*0.12

    importantdata.to_excel(output_path, index=False)

    # Check if the file was saved successfully
    if output_path.exists():
        return str(output_path)
    else:
        return None