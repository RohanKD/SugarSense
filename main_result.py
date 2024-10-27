import json

from apple_watch import process_apple_watch_data
from ecg import process_ecg_data
from ecg_analysis import analyze_ecg_data
from food_insulin import process_food_insulin_data
from libre import analyze_blood_sugar_report
from predict_retina import train_and_predict_retinopathy
from retina import process_retina_images
from diabetica_llm import analyze_health_data


from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
import os

def main():
    apple_watch_file = 'data/apple_watch.csv'
    ecg_file = 'data/ecg_data.csv'
    food_file = 'data/food_data.csv'
    insulin_file = 'data/insulin_data.csv'
    blood_sugar_report = 'data/blood_sugar_report.pdf'
    retina_images_path = 'data/retina_images/'
    retinopathy_model = 'model.h5'
    date_filter = '2023-10-15'


    apple_watch_data = process_apple_watch_data(apple_watch_file, date_filter)

    ecg_data = process_ecg_data(ecg_file)
    ecg_analysis_results = analyze_ecg_data(ecg_data)

    food_insulin_data = process_food_insulin_data(food_file, insulin_file, date_filter)

    blood_sugar_analysis = analyze_blood_sugar_report(blood_sugar_report)

    retina_image_data = process_retina_images(retina_images_path)
    
    retinopathy_results = predict_on_images(retina_images_path, retinopathy_model)


    combined_data = {
        'apple_watch': apple_watch_data,
        'ecg': ecg_analysis_results,
        'food_insulin': food_insulin_data,
        'blood_sugar': blood_sugar_analysis,
        'retinopathy': retinopathy_results,
        'retina_images': retina_image_data,
    }

    llm_output = analyze_health_data(combined_data)

    anthropic_api_key = "YOUR_ANTHROPIC_API_KEY"
    formatted_output = send_to_claude(llm_output, anthropic_api_key)

    create_pdf(formatted_output, 'health_report.pdf')

    print("Health report has been generated and saved as 'health_report.pdf'.")

def send_to_claude(content, anthropic_api_key):
    from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

    client = Anthropic(api_key=anthropic_api_key)

    prompt = f"""
Please format the following health report content into a well-structured and professional report suitable for a PDF document. Provide the output in HTML format:

{content}

Include headings, bullet points, and any other formatting that enhances readability.
"""

    response = client.completions.create(
        model="claude-v1",
        max_tokens_to_sample=3000,
        prompt=f"{HUMAN_PROMPT}{prompt}{AI_PROMPT}"
    )


    formatted_content = response.completion.strip()

    return formatted_content

def create_pdf(content, output_file):
    from weasyprint import HTML


    HTML(string=content).write_pdf(output_file)

if __name__ == '__main__':
    main()
