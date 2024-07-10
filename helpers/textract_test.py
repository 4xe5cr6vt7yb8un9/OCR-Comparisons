import requests
from textractcaller.t_call import call_textract
from textractprettyprinter.t_pretty_print import get_string
from helpers.utils import log_transcription

def process_transcription_textract(data):
    url = data.get('image_url')

    print(f"Transcribing image: {url}")

    image = requests.get(url, stream=True).content
    manual_text = data.get("image_text")
    
    textract_output = call_textract(input_document=image)
    extracted_text = get_string(textract_json=textract_output).replace("\n\n", " ")

    log_transcription(extracted_text, manual_text, "Textract", "none", url)

    print("Finished transcription\n")

