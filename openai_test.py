import sys
from openai import OpenAI
from dotenv import load_dotenv 
from utils import extract_json, log_transcription

# Use ChatGPT to transcribe the given image
def transcribe_image(url, prompt, client):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text", 
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": url,
                        },
                    },
                ],
            }
        ],
        max_tokens=1024,
    )
    return response

def process_transcription(data, prompt, client):
    url = data.get('image_url')

    print(f"Transcribing image: {url}")

    response = transcribe_image(url, prompt, client)
    extracted_text = response.choices[0].message.content
    manual_text = data.get("image_text")

    log_transcription(extracted_text, manual_text, response.model, prompt, url)

    print("Finished transcription\n")


load_dotenv() 

client = OpenAI()
prompt = "Please transcribe the text from the following image with high accuracy. Ensure that all punctuation, capitalization, and formatting are preserved as closely as possible to the original. If any part of the text is illegible or unclear, indicate this with '[illegible]' in the transcription. Pay special attention to names, dates, and any specific terminology. Please provide only the transcription."
test_data = extract_json('testing_data.json')

if (len(sys.argv) > 1):
    num = int(sys.argv[1])
    data = test_data.get('data', [])[num]
    process_transcription(data, prompt, client)
else:
    for data in test_data.get('data', []):
        process_transcription(data, prompt, client)
    
