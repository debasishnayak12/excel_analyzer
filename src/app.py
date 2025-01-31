from flask import Flask, request, render_template, jsonify, send_file,url_for,send_from_directory
from werkzeug.utils import secure_filename
import os
import pandas as pd
import numpy as np
import uuid

from mmt import mmt_result
from stayflexi import stayflexi
from old_pending import update_pending
from bking import stayflexiBookingcom,cancelled
from jointreport import jointreport

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'docs/files'

ALLOWED_EXTENSIONS = {'xlsx','csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB limit

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
REPORT_FOLDER = os.path.join(PROJECT_ROOT, 'docs', 'report')
# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'file1' not in request.files or 'file2' not in request.files:
        return jsonify({'status': False, 'message': 'Both files are required!'}), 400

    file1 = request.files['file1']
    file2 = request.files['file2']
    file3 = request.files.get('file3')  # Optional file
    file4 = request.files.get('file4')  # Optional file
    bookingcomcheck = request.form.get('bookingcheck')
    commission = (int(request.form.get('sliderValue')))/100
    print("commission:",commission)
    # if not commission or not commission.isdigit():
    #     commission = 30

    print("file1:", file1)
    print("file2:", file2)

    if file1 and allowed_file(file1.filename) and file2 and allowed_file(file2.filename):
        filename1 = secure_filename(file1.filename)
        filename2 = secure_filename(file2.filename)

        file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
        file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))

        file3 = request.files.get('file3')  # Optional file
        file4 = request.files.get('file4')  # Optional file

        if file3 and allowed_file(file3.filename):
            filename3 = secure_filename(file3.filename)
            file3.save(os.path.join(app.config['UPLOAD_FOLDER'], filename3))
            # Optionally process file3 if needed
        if file4 and allowed_file(file4.filename):
            filename4 = secure_filename(file4.filename)
            file4.save(os.path.join(app.config['UPLOAD_FOLDER'], filename4))

        if file3 and file4:
            print("file3 and file4")
            old_final_data_path = update_pending(os.path.join(app.config['UPLOAD_FOLDER'], filename3),os.path.join(app.config['UPLOAD_FOLDER'], filename4))
            old_data = pd.read_excel(old_final_data_path)
        else:
            old_data = None

        try:
            print('start stayflexipath')
            stayflexipath = stayflexi(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
            if not stayflexipath or not os.path.exists(stayflexipath):
                return jsonify({'status': False, 'message': 'Error processing file1'}), 500
            print('stayflexipath:', stayflexipath)
            

            print('start mmt')
            final_data_path = mmt_result(os.path.join(app.config['UPLOAD_FOLDER'], filename2), stayflexipath)
            if not final_data_path or not os.path.exists(final_data_path):
                return jsonify({'status': False, 'message': 'Error processing file2'}), 500
            print('final_data_path:', final_data_path)

            final_data = pd.read_excel(final_data_path)
            print("final_data:",final_data)
            if old_data is not None:
                final_data = pd.concat([final_data, old_data], ignore_index=True)
                # final_data.drop_duplicates(subset=['BookingID', 'Customer Name', 'Booking Vendor', 'Check-in', 'Check-out'], inplace=True)
                print("final_data after concat:",final_data)   

            print("old data is none") 

            # final_data['GST on commission'] = ((final_data['Room Charges (A)']) * 0.30) * 0.18
            # final_data['TB commission'] = ((final_data["Room Charges (A)"]) * 0.30)
            # final_data['PayToHotel'] = final_data['Room Charges (A)'] - (
            #     final_data['GST on commission'] + ((final_data["Room Charges (A)"]) * 0.30)
            # )
            final_data['GST on commission'] = ((final_data['Room Charges (A)']) * commission) * 0.18
            final_data['TB commission'] = ((final_data["Room Charges (A)"]) * commission)
            final_data['PayToHotel'] = final_data['Room Charges (A)'] - (
                final_data['GST on commission'] + ((final_data["Room Charges (A)"]) * (commission))
            )
            final_data['final commission'] = final_data['Amount Paid'] - final_data['PayToHotel']

            print("final dat acoluumns :",final_data.columns)
            pay_to_hotel_sum = final_data['PayToHotel'].sum()
            print("pay_to_hotel_sum:", pay_to_hotel_sum)
            final_commission_sum = final_data['final commission'].sum()
            print("final_commission_sum:", final_commission_sum)
            total_amount_paid = final_data['Amount Paid'].sum()
            print("total_amount_paid:", total_amount_paid)

            

            # Create a new row with NaN for other columns and the sums for 'PayToHotel' and 'FinalCommission'
            new_row = {
                'BookingID': f"After ({100*commission}%) Total",  # or you can use None if you prefer
                'Customer Name': np.nan,
                'Booking Vendor': np.nan,
                'Room Charges (A)': np.nan,
                'Amount Paid': np.round(total_amount_paid),
                'Payment Status': np.nan,
                'Check-in': np.nan,
                'Check-out': np.nan,
                'Payment Date': np.nan,
                'GST on commission': np.nan,
                'TB commission': np.nan,
                'PayToHotel': np.round(pay_to_hotel_sum),
                'final commission': np.round(final_commission_sum)
            }


            new_df = pd.DataFrame([new_row])
            print("new_df:",new_df)
            print("shape of after append final data:",final_data.shape)
            final_data = pd.concat([final_data, new_df], ignore_index=True)

            print("shape of after append final data:",final_data.shape)

            if bookingcomcheck == 'Yes':
                print("bookingcomcheck is on")
                bookingcompath = stayflexiBookingcom(os.path.join(app.config['UPLOAD_FOLDER'], filename1),commission)
                print("bookingcompath:",bookingcompath)
                dookingdata = pd.read_excel(bookingcompath)
                finaldatapath =  jointreport(final_data,dookingdata)
                print("bkng data path :",finaldatapath)
                final_data = pd.read_excel(finaldatapath)
                print("bkng data path 2:",bookingcompath)


            os.makedirs('docs/report', exist_ok=True)
            unique_id = uuid.uuid4().hex
            print("unique_id:", unique_id)
            report_filename = f'report_{unique_id}_.xlsx'
            print("report_filename:", report_filename)
            report_path = os.path.join('docs/report', report_filename)
            final_data.to_excel(report_path, index=False)

            print("final data excel made successfully")

            # download_url = url_for('download_file', filename=report_filename, _external=True)

            print("report path:", report_path)

            return jsonify({
                'status': True,
                'message': 'Files processed successfully!',
                'download_url': f'/download/{report_filename}',
                'download_name': report_filename
            })
        except Exception as e:
            return jsonify({'status': False, 'message': f'Error: {str(e)}'}), 500
    else:
        return jsonify({'status': False, 'message': 'Only .xlsx files are allowed!'}), 400
    

@app.route('/bookingcomreport', methods=['POST'])
def bkngcomreport():
    if 'file1' not in request.files :
        return jsonify({'status': False, 'message': 'stayflexi file  required!'}), 400

    file1 = request.files.get('file1')
    commission = (int(request.form.get('sliderValue')))/100
    print("commission:",commission)
    # file2 = request.files.get('file2')
    # file3 = request.files.get('file3')  # Optional file
    # file4 = request.files.get('file4')  # Optional file
    # commission = (int(request.form.get('sliderValue')))/100
    
    # if not commission or not commission.isdigit():
    #     commission = 30

    print("file1:", file1)

    if file1 and allowed_file(file1.filename):
            filename1 = secure_filename(file1.filename)
            file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
            # Optionally process file3 if needed

        
    try:
        
        bookingcompath = stayflexiBookingcom((os.path.join(app.config['UPLOAD_FOLDER'], filename1)),commission)
        print("bkng data path :",bookingcompath)

        
        final_df = pd.read_excel(bookingcompath)

        os.makedirs('docs/report', exist_ok=True)
        unique_id = uuid.uuid4().hex
        print("unique_id:", unique_id)
        report_filename = f'bookingcom_report_{unique_id}_.xlsx'
        print("report_filename:", report_filename)
        report_path = os.path.join('docs/report', report_filename)
        final_df.to_excel(report_path, index=False)

        print("final data excel made successfully")

        # download_url = url_for('download_file', filename=report_filename, _external=True)

        print("report path:", report_filename)

        return jsonify({
            'status': True,
            'message': 'Files processed successfully!',
            'download_url': f'/download/{report_filename}',
            'download_name': report_filename
        })
    except Exception as e:
        return jsonify({'status': False, 'message': f'Error: {str(e)}'}), 500
    
    
@app.route('/cancelled', methods=['POST'])
def bkngcomcancelled():
    if 'file1' not in request.files :
        return jsonify({'status': False, 'message': 'stayflexi file  required!'}), 400

    file1 = request.files.get('file1')
    # commission = (int(request.form.get('sliderValue')))/100
    # print("commission:",commission)
    # file2 = request.files.get('file2')
    # file3 = request.files.get('file3')  # Optional file
    # file4 = request.files.get('file4')  # Optional file
    # commission = (int(request.form.get('sliderValue')))/100
    
    # if not commission or not commission.isdigit():
    #     commission = 30

    print("file1:", file1)

    if file1 and allowed_file(file1.filename):
            filename1 = secure_filename(file1.filename)
            file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
            # Optionally process file3 if needed

        
    try:
        
        bookingcompath = cancelled(os.path.join(app.config['UPLOAD_FOLDER'], filename1))

        
        final_df = pd.read_excel(bookingcompath)

        os.makedirs('docs/report', exist_ok=True)
        unique_id = uuid.uuid4().hex
        print("unique_id:", unique_id)
        report_filename = f'bookingcom_cancelled_{unique_id}_.xlsx'
        print("report_filename:", report_filename)
        report_path = os.path.join('docs/report', report_filename)
        final_df.to_excel(report_path, index=False)

        print("final data excel made successfully")

        # download_url = url_for('download_file', filename=report_filename, _external=True)

        print("report path:", report_filename)

        return jsonify({
            'status': True,
            'message': 'Files processed successfully!',
            'download_url': f'/download/{report_filename}',
            'download_name': report_filename
        })
    except Exception as e:
        return jsonify({'status': False, 'message': f'Error: {str(e)}'}), 500
    

@app.route('/download/<filename>')
def download_file(filename):
    
    try:
        # Get absolute path
        report_path = os.path.join(REPORT_FOLDER, filename)

        if not os.path.exists(report_path):
            print("🚨 File not found on the server!")
            return jsonify({'status': False, 'message': 'File not found!'}), 404

        return send_file(
            report_path,
            as_attachment=True,
            # download_name=f'{filename2}_report.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
    except Exception as e:
        return jsonify({'status': False, 'message': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
