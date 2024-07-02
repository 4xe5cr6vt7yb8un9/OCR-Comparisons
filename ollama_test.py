import json
import requests
from PIL import Image

from langchain_community.llms import Ollama

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

llm = Ollama(model='llama3')

url = test_data[0][0]
image = Image.open(requests.get(url, stream=True).raw).convert("RGB")
image.show()

res = llm.invoke("Transcribe this image: "+url)
print(res)