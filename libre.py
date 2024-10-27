import requests
from pypdf import PdfReader
from anthropic import Anthropic

def extract_text_from_pdf(file_path):
    text = ""
    reader = PdfReader(file_path)
    for page in reader.pages:
        text += page.extract_text()
    return text

file_path = "/Users/rohan/Downloads/DilipDalal_10-26-2024.pdf"
pdf_text = extract_text_from_pdf(file_path)

client = Anthropic(api_key="APIKEYREMOVED")
MODEL_NAME = "claude-3-5-sonnet-20241022"

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


prompt = f"""
Here is a glucose report for patient + {file_path}:
<report>{pdf_text}</report>

Please perform the following tasks:
1. Summarize the glucose report, highlighting average levels, time-in-range, and variability.
2. Provide specific recommendations for managing diabetes based on the glucose patterns.
Use <summary_insights> tags for the summary and <recommendations> tags for the recommendations.
"""


completion = get_completion(client, MODEL_NAME, prompt)
print("Claude Response:\n", completion)
