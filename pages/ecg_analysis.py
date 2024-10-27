import os
import google.generativeai as genai
def ecg(rr_intervals, qt_intervals, ecg_image_path):
    my_api_key = os.environ.get("AIzaSyBiFUDnsXW9tEuuXZ0O9Y5Ym8_gYQQ2YKA")
    genai.configure(api_key="AIzaSyBiFUDnsXW9tEuuXZ0O9Y5Ym8_gYQQ2YKA")

    additional_clinical_info = "Patient with type 2 diabetes"

    rr_intervals_str = ', '.join(map(str, rr_intervals))
    qt_intervals_str = ', '.join(map(str, qt_intervals))

    prompt = f"""
    Analyze the following ECG data for a diabetic patient:
    * **QRS duration:** Not available in this prompt but should be inferred from the image (image not provided)
    * **QT intervals:** [{qt_intervals_str}] ms
    * **RR intervals:** [{rr_intervals_str}] ms
    * **Other relevant clinical information:** {additional_clinical_info}
    
    Based on the ECG data, please assess if the patient shows predispositions to heart conditions related to diabetes. Provide any notable findings, risk factors, and suggestions for further evaluation or treatment.
    """

    model = genai.GenerativeModel("gemini-1.5-flash")
    result = model.generate_content(
        [ecg_image_path, "\n\n", prompt]
    )



    return result.text
