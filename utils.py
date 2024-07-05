import json
import requests
from PIL import Image
from os.path import exists
from datetime import datetime

from compare import word_distance, cos_similarity, percentage_correct


# Function for finding the greatest common factor between two numbers
def gcf(a, b):
    if (not a >= b):
        a, b = b, a

    r = a % b
    if r == 0:
        return b
    else:
        return gcf(b, r)


# Extracts testing data from json
def extract_json(file_path):
    # Load the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    return data

# Logs information about the transcription to compare
def log_transcription(message, original, model, prompt, url):
    file = url.rsplit('/', 1)[-1].split('.')[0]

    image = Image.open(requests.get(url, stream=True).raw).convert("RGB")
    size = image.size
    div = int(gcf(size[0], size[1]))

    message = message.replace('\n', ' ')
    original = original.replace('\n', ' ')

    distance = word_distance([message, original])
    similarity = cos_similarity(message, original)
    correct = percentage_correct(message, original)

    info = {
        "date": datetime.now().strftime('%m-%d-%Y'),
        "model": model,
        "prompt": prompt,
        "extracted_text": message,
        "original_text": original,
        "image_data": {
            "width": size[0],
            "height": size[1],
            "aspect_ratio": f"{size[0]/div:.0f}:{size[1]/div:.0f}",
        },
        "validation": {
            "word_distance": "%.4f" % distance,
            "cos_similarity": "%.4f" % similarity,
            "matching_words_row": "%.0f" % correct,
        }
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