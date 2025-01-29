# import pandas as pd
# import os
# from pathlib import Path

# def stayflexi(file):
    # try:
    #     file_path = Path(file)

    #     # Ensure the file exists before proceeding
    #     if not file_path.exists():
    #         return {'status': False, 'message': 'File not found!'}

    #     # Load the Excel data
    #     try:
    #         _,ext = os.path.splitext(file_path)
    #         if ext == '.xlsx':
    #             data = pd.read_excel(file_path, engine='openpyxl')  # Use openpyxl for .xlsx
    #         else:
    #             data = pd.read_csv(file_path)
    #     except Exception as e:
    #         return {'status': False, 'message': f'Error reading file: {str(e)}'}

    #     # Check if required columns exist
    #     required_columns = {'Source', 'Booking Status', 'Check In Date', 'Check Out Date'}
    #     missing_columns = required_columns - set(data.columns)
    #     if missing_columns:
    #         return {'status': False, 'message': f'Missing columns: {", ".join(missing_columns)}'}

    #     # Filter the data
    #     filtered_data = data[
    #         (data['Source'].isin(['GOIBIBO', 'MAKEMYTRIP'])) &
    #         (data['Booking Status'].str.upper() == 'CONFIRMED')
    #     ].copy()  # Avoid SettingWithCopyWarning

        

    #     # Convert date columns safely
    #     for col in ['Check In Date', 'Check Out Date']:
    #         try:
    #             filtered_data[col] = pd.to_datetime(
    #                 filtered_data[col], format='%d/%m/%Y', errors='coerce'
    #             ).dt.strftime('%Y-%m-%d')
    #         except Exception:
    #             return {'status': False, 'message': f'Invalid date format in column: {col}'}

    #     # Define output path
    #     output_dir = Path('docs/files')
    #     output_dir.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
    #     output_path = output_dir / f'confirmed_{file_path.name}'

    #     # Save filtered data
    #     try:
    #         filtered_data.to_excel(output_path, index=False, engine='openpyxl')
    #     except Exception as e:
    #         return {'status': False, 'message': f'Error saving file: {str(e)}'}

    #     # Verify if the file was saved
    #     if output_path.exists():
    #         return {'status': True, 'path': str(output_path)}
    #     else:
    #         return {'status': False, 'message': 'Failed to save the file!'}

    # except Exception as e:
    #     return {'status': False, 'message': f'Unexpected error: {str(e)}'}


import pandas as pd
import os
from pathlib import Path

def stayflexi(file):
    # Load the data
    data = pd.read_excel(file)

    # Filter the data
    filtered_data = data[
        data['Source'].isin(['GOIBIBO', 'MAKEMYTRIP']) & 
        (data['Booking Status'] == 'CONFIRMED')
    ]
    
    # Convert date columns
    filtered_data.loc[:, 'Check In Date'] = pd.to_datetime(
        filtered_data['Check In Date'], format='%d/%m/%Y'
    ).dt.strftime('%Y-%m-%d')
    filtered_data.loc[:, 'Check Out Date'] = pd.to_datetime(
        filtered_data['Check Out Date'], format='%d/%m/%Y'
    ).dt.strftime('%Y-%m-%d')

    # Create the output directory if it doesn't exist
    os.makedirs('docs/files', exist_ok=True)
    output_path = Path('docs/files') / f'confirmed_{Path(file).name}'

    # Save the filtered data to the specified path
    filtered_data.to_excel(output_path, index=False)

    # Check if the file was saved successfully
    if output_path.exists():
        return str(output_path)
    else:
        return None
