import sys
import anthropic
from openai import OpenAI
from dotenv import load_dotenv 

from utils import extract_json
from openai_test import process_transcription_gpt
from anthropic_test import process_transcription_claude


def transcribe_docs(data, prompt, gpt, claude, model):
    match (model):
        case ("openai"):
            process_transcription_gpt(data, prompt, gpt)
        case ("anthropic"):
            process_transcription_claude(data, prompt, claude)
        case ("all"):
            process_transcription_gpt(data, prompt, gpt)
            process_transcription_claude(data, prompt, claude)
    

def main():
    load_dotenv()

    if (len(sys.argv) < 1):
        print("Please provide which model to use; openai, anthropic, or all")
        return

    gpt = OpenAI()
    claude = anthropic.Anthropic()

    prompt = "Please transcribe the text from the following image with high accuracy. Ensure that all punctuation, capitalization, and formatting are preserved as closely as possible to the original. If any part of the text is illegible or unclear, indicate this with '[illegible]' in the transcription. Pay special attention to names, dates, and any specific terminology. Please provide only the transcription."
    test_data = extract_json('testing_data.json')
    
    model = sys.argv[1].lower()

    if (len(sys.argv) > 2):
        num = int(sys.argv[2])
        data = test_data.get('data', [])[num]
        transcribe_docs(data, prompt, gpt, claude, model)
        return
    
    for data in test_data.get('data', []):
        transcribe_docs(data, prompt, gpt, claude, model)   
        

if __name__ == "__main__":
    main()