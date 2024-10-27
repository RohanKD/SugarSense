
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
def ecg(file_path):
    ecg_data = pd.read_csv(file_path, skiprows=14, header=None, names=['Voltage'])

    sample_rate = 512  # in Hz
    time = np.arange(len(ecg_data)) / sample_rate

    # Detect R-peaks (QRS complexes) in the ECG signal
    peaks, _ = find_peaks(ecg_data['Voltage'], distance=sample_rate*0.6, height=200)
    plt.figure(figsize=(12, 6))
    plt.plot(time, ecg_data['Voltage'], label='ECG Signal')
    plt.plot(time[peaks], ecg_data['Voltage'][peaks], 'rx', label='QRS Complex (R Peaks)')
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (µV)')
    plt.title('ECG Signal with Detected QRS Complexes')
    plt.legend()
    plt.show()

    # Calculate RR intervals and approximate QT intervals
    rr_intervals = np.diff(time[peaks])
    qt_intervals = 0.36 * rr_intervals ** 0.5  # Using Bazett's formula for QT approximation
    
    print("RR Intervals (s):", rr_intervals)
    print("Approximated QT Intervals (s):", qt_intervals)
