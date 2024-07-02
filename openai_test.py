import json
import requests
from PIL import Image

from openai import OpenAI

def extract_json(file_path):
    test_data = []
    # Load the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Extract and display the relevant information from each document
    documents = data.get("data", [])
    for doc in documents:
        image_url = doc.get("image_url", "No URL provided")
        image_text = doc.get("image_text", "No text provided")
        quality = doc.get("quality", "No quality description provided")
        date = doc.get("date", "No date provided")

        data = [image_url, image_text, quality, date]
        test_data.append(data)

    return test_data

test_data = extract_json('testing_data.json')

url = test_data[6][0]
image = Image.open(requests.get(url, stream=True).raw).convert("RGB")
image.show()

client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {
      "role": "user",
      "content": [
        {
         "type": "text", 
         "text": "Transcribe this image as accurately as possible"},
        {
          "type": "image_url",
          "image_url": {
            "url": url,
          },
        },
      ],
    }
  ],
  max_tokens=500,
)

print(response.choices[0].message.content)