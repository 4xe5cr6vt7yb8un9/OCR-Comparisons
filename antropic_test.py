import anthropic
import base64
import httpx

from dotenv import load_dotenv
from utils import extract_json, log_transcription

load_dotenv() 

def transcribe_image(url, prompt, client):
    image1_media_type = "image/jpeg"
    image1_data = base64.b64encode(httpx.get(url).content).decode("utf-8")

    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": image1_media_type,
                            "data": image1_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ],
            }
        ],
    )
    return message


test_data = extract_json('testing_data.json')

client = anthropic.Anthropic()
prompt = "Please transcribe the text from the following image with high accuracy. Ensure that all punctuation, capitalization, and formatting are preserved as closely as possible to the original. If any part of the text is illegible or unclear, indicate this with '[illegible]' in the transcription. Pay special attention to names, dates, and any specific terminology. Please provide only the transcription. Do not say anything like 'Here is the transcription of the image'"

data = test_data.get('data', [])[0]

for data in test_data.get('data', []):
    url = data.get('image_url')

    print(f"Transcribing image: {url}")

    response = transcribe_image(url, prompt, client)
    extracted_text = response.content[0].text
    manual_text = data.get("image_text")

    log_transcription(extracted_text, manual_text, response.model, prompt, url)

    print("Finished transcription\n")