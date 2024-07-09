import base64
import httpx

from utils import log_transcription


# Handles the api request for claude
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

# Transcribes the image using Claude
def process_transcription_claude(data, prompt, client):
    url = data.get('image_url')

    print(f"Transcribing image: {url}")

    response = transcribe_image(url, prompt, client)
    extracted_text = response.content[0].text
    manual_text = data.get("image_text")

    log_transcription(extracted_text, manual_text, response.model, prompt, url)

    print("Finished transcription\n")

    