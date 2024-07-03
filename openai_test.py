from openai import OpenAI
from dotenv import load_dotenv 
from utils import extract_json, log_transcription
from compare import word_distance

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

load_dotenv() 

client = OpenAI()
prompt = "Please transcribe the text from the following image with high accuracy. Ensure that all punctuation, capitalization, and formatting are preserved as closely as possible to the original. If any part of the text is illegible or unclear, indicate this with '[illegible]' in the transcription. Pay special attention to names, dates, and any specific terminology. Please provide only the transcription."
test_data = extract_json('testing_data.json')

data = test_data.get('data', [])[2]

for data in test_data.get('data', []):
    url = data.get('image_url')

    print(f"Transcribing image: {url}")
    response = transcribe_image(url, prompt, client)
    extracted_text = response.choices[0].message.content
    print("Finished transcription")

    # Calculates the distance between the automatted and manual transcriptions
    print("Calculating word distance")
    manual_text = data.get("image_text")
    distance = word_distance([extracted_text, manual_text])
    print('The transcription has a distance of %.4F\n' % distance)

    log_transcription(extracted_text, response.model, distance, prompt, url)
