from flask import Flask, request, render_template, jsonify, send_file,url_for,send_from_directory
from werkzeug.utils import secure_filename
import os
import pandas as pd
import uuid

from mmt import mmt_result
from stayflexi import stayflexi

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'docs/files'

ALLOWED_EXTENSIONS = {'xlsx'}
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

    if file1 and allowed_file(file1.filename) and file2 and allowed_file(file2.filename):
        filename1 = secure_filename(file1.filename)
        filename2 = secure_filename(file2.filename)

        file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
        file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))

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
            final_data['gst on commssion'] = ((final_data['Room Charges (A)']) * 0.30) * 0.18
            final_data['GST TB commission'] = ((final_data["Room Charges (A)"]) * 0.30)
            final_data['PayToHotel'] = final_data['Room Charges (A)'] - (
                final_data['gst on commssion'] + ((final_data["Room Charges (A)"]) * 0.30)
            )
            final_data['final commission'] = final_data['Amount Paid'] - final_data['PayToHotel']

            os.makedirs('docs/report', exist_ok=True)
            unique_id = uuid.uuid4().hex
            report_filename = f'report_{unique_id}_{filename2}'
            report_path = os.path.join('docs/report', report_filename)
            final_data.to_excel(report_path, index=False)

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
