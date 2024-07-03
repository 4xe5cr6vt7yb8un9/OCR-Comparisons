import json
import requests
from PIL import Image
from os.path import exists


# Extracts testing data from json
def extract_json(file_path):
    # Load the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    return data

# Logs information about the transcription to compare
def log_transcription(message, model, distance, prompt, url):
    file = url.rsplit('/', 1)[-1].split('.')[0]

    image = Image.open(requests.get(url, stream=True).raw).convert("RGB")
    size = image.size

    info = {
        "model": model,
        "prompt": prompt,
        "message": message,
        "aspect_ratio": f"{size[0]}:{size[1]}",
        "word_distance": "%.4f" % distance,
    }
    output_file = f"logs/{file}.json"

    if not exists(output_file):
        with open(output_file,'w') as file:
            json.dump({"transcripts": [info]}, file, indent = 4)
    else:
        with open(output_file,'r+') as file:
            file_data = json.load(file)
            file_data["transcripts"].append(info)
            file.seek(0)
            json.dump(file_data, file, indent = 4)