from utils import log_transcription

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

def process_transcription_gpt(data, prompt, client):
    url = data.get('image_url')

    print(f"Transcribing image: {url}")

    response = transcribe_image(url, prompt, client)
    extracted_text = response.choices[0].message.content
    manual_text = data.get("image_text")

    log_transcription(extracted_text, manual_text, response.model, prompt, url)

    print("Finished transcription\n")
