from flask import Flask, request, jsonify, send_file, send_from_directory
import pandas as pd
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
from io import BytesIO
from PyPDF2 import PdfReader
from anthropic import Anthropic
import os
from flask_cors import CORS
from scipy.signal import find_peaks
import numpy as np
from ecg_analysis import ecg
from PIL import Image

app = Flask(__name__)
CORS(app)
    
@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if not file.filename.endswith('.csv'):
        return jsonify({"error": "Only CSV files are allowed"}), 400
    start_date_str = request.form.get('start_date')
    end_date_str = request.form.get('end_date')
    
    if not start_date_str or not end_date_str:
        return jsonify({"error": "Start date and end date are required"}), 400

    try:
        start_date = pd.to_datetime(start_date_str).tz_localize('UTC')
        end_date = pd.to_datetime(end_date_str).tz_localize('UTC')
    except Exception as e:
        return jsonify({"error": f"Invalid date format: {str(e)}"}), 400

    data = pd.read_csv(file)

    if 'startDate' not in data.columns or 'value' not in data.columns:
        return jsonify({"error": "CSV must contain 'startDate' and 'value' columns"}), 400

    data['startDate'] = pd.to_datetime(data['startDate'], errors='coerce')
    data = data.dropna(subset=['startDate', 'value'])
    data = data[(data['startDate'] >= start_date) & (data['startDate'] <= end_date)]

    rolling_window = 7
    data['rolling_avg'] = data['value'].rolling(window=rolling_window, center=True).mean()

    plt.figure(figsize=(12, 6))
    plt.plot(data['startDate'], data['rolling_avg'], label=f'{rolling_window}-Day Rolling Average', 
             color='#2D799C', linewidth=1.5)
    plt.title('Steps Over Time (with Rolling Average)')
    plt.xlabel('Start Date')
    plt.ylabel('Steps')
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()


    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')
@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if not file.filename.endswith('.pdf'):
        return jsonify({"error": "Only PDF files are allowed"}), 400

    blood_data = []
    reader = PdfReader(file)

    for page in reader.pages:
        text = page.extract_text()
        
    
        lines = text.split('\n')
        for line in lines:
            if "Date:" in line and "Level:" in line:
                parts = line.split(" ")
                date = parts[1]
                level = parts[-2]
                blood_data.append({
                    "date": date,
                    "level": int(level)  
                })

    return jsonify(blood_data)

API_KEY = ""
client = Anthropic(api_key=API_KEY)
MODEL_NAME = "claude-3-5-sonnet-20241022" 

def extract_text_from_pdf(file):
    """Extract text from a PDF file object."""
    text = ""
    reader = PdfReader(file)
    for page in reader.pages:
        text += page.extract_text()
    return text


def get_completion(client, model_name, prompt):
    response = client.messages.create(
        model=model_name,
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )
    return response.content[0].text

@app.route('/analyze-pdf', methods=['POST'])
def analyze_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if not file.filename.endswith('.pdf'):
        return jsonify({"error": "Only PDF files are allowed"}), 400

    pdf_text = extract_text_from_pdf(file)

    prompt = f"""
    Here is a glucose report for the patient:
    <report>{pdf_text}</report>

    Please perform the following tasks:
    1. Summarize the glucose report, highlighting average levels, time-in-range, and variability.
    2. Provide specific recommendations for managing diabetes based on the glucose patterns.
    Use <summary_insights> tags for the summary and <recommendations> tags for the recommendations.
    """

    try:
        print(client)
        print(MODEL_NAME)
        print(prompt)
        completion = get_completion(client, MODEL_NAME, prompt)
    except Exception as e:
        return jsonify({"error": f"Failed to analyze PDF: {str(e)}"}), 500

    return jsonify({"analysis": completion})
@app.route('/analyze-ecg', methods=['POST'])
def analyze_ecg():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if not file.filename.endswith('.csv'):
        return jsonify({"error": "Only CSV files are allowed"}), 400

    try:

        ecg_data = pd.read_csv(file, skiprows=14, header=None, names=['Voltage'])

        sample_rate = 512  
        time = np.arange(len(ecg_data)) / sample_rate

        peaks, _ = find_peaks(ecg_data['Voltage'], distance=sample_rate * 0.6, height=200)
        plt.figure(figsize=(12, 6))
        plt.plot(time, ecg_data['Voltage'], label='ECG Signal')
        plt.plot(time[peaks], ecg_data['Voltage'][peaks], 'rx', label='QRS Complex (R Peaks)')
        plt.xlabel('Time (s)')
        plt.ylabel('Voltage (µV)')
        plt.title('ECG Signal with Detected QRS Complexes')
        plt.legend()


        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()

        rr_intervals = np.diff(time[peaks]).tolist() 
        qt_intervals = (0.36 * np.sqrt(rr_intervals)).tolist()  
        pil_image = Image.open(img)
        x = ecg(rr_intervals, qt_intervals, pil_image)
        print(x)
        return send_file(img, mimetype='image/png')
    
        '''
        

        return jsonify({
            "rr_intervals": rr_intervals,
            "qt_intervals": qt_intervals
        })
        '''
    except Exception as e:
        print("Error processing ECG data:", e)
        return jsonify({"error": f"Failed to analyze ECG: {str(e)}"}), 500
@app.route('/ecg-plot', methods=['GET'])
def ecg_plot():
    global ecg_data_cache

    if not ecg_data_cache:
        return jsonify({"error": "No ECG data available. Please analyze ECG first."}), 400

    try:
        time = ecg_data_cache['time']
        voltage = ecg_data_cache['voltage']
        peaks = ecg_data_cache['peaks']

        plt.figure(figsize=(12, 6))
        plt.plot(time, voltage, label='ECG Signal')
        plt.plot(time[peaks], voltage.iloc[peaks], 'rx', label='QRS Complex (R Peaks)')
        plt.xlabel('Time (s)')
        plt.ylabel('Voltage (µV)')
        plt.title('ECG Signal with Detected QRS Complexes')
        plt.legend()

        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()

        return send_file(img, mimetype='image/png')

    except Exception as e:
        print("Error generating ECG plot:", e)
        return jsonify({"error": f"Failed to generate ECG plot: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
