from helpers.utils import log_transcription

# Handles the api request for ChatGPT
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
        temperature=0.3,
    )
    return response

# Use ChatGPT to transcribe the given image
def process_transcription_gpt(data, prompt, client):
    url = data.get('objectUrl')

    print(f"Transcribing image: {url}")

    response = transcribe_image(url, prompt, client)
    extracted_text = response.choices[0].message.content
    tokens = response.usage.total_tokens
    manual_text = data.get("extractedText")

    log_transcription(extracted_text, manual_text, response.model, tokens, prompt, data)

    print("Finished transcription\n")
