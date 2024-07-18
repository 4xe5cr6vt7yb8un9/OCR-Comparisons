import sys
import anthropic
from openai import OpenAI
from dotenv import load_dotenv 

from helpers.utils import extract_json
from helpers.openai_test import process_transcription_gpt
from helpers.anthropic_test import process_transcription_claude
from helpers.textract_test import process_transcription_textract

# Handles which model needs to be used for the transcription process
def transcribe_docs(data, prompt, gpt, claude, model):
    match (model):
        case ("openai"):
            process_transcription_gpt(data, prompt, gpt)
        case ("anthropic"):
            process_transcription_claude(data, prompt, claude)
        case ("textract"):
            process_transcription_textract(data)
        case ("all"):
            process_transcription_gpt(data, prompt, gpt)
            process_transcription_claude(data, prompt, claude)
            process_transcription_textract(data)
    
# Main function for transcribing
def main():
    load_dotenv()

    if (len(sys.argv) < 1):
        print("Please provide which model to use; openai, anthropic, textract, or all")
        return

    # Initialize the clients for each model
    gpt = OpenAI()
    claude = anthropic.Anthropic()

    # Prepare the prompt and extract the testing dataset
    prompt = '''
Prompt:
You are tasked with transcribing a given document. Your goal is to accurately convert the text from
the document into a typed format, preserving the original content as closely as possible.

Please follow these instructions for transcription:

1. Read through the entire document carefully before beginning the transcription.
2. Transcribe the text exactly as it appears, including any spelling errors, punctuation, or unusual
formatting.
3. Preserve line breaks and paragraph structures as they appear in the original document.
4. If there are any headings, subheadings, or different text styles (e.g., bold, italic), indicate
them using appropriate markdown syntax (e.g., # for headings, ** for bold, * for italic).
5. If there are any tables, try to recreate them using markdown table syntax.
6. For any images, insert a placeholder text like [IMAGE] where the image appears in the document.

If you encounter any parts of the text that are unclear or difficult to read:
1. Make your best guess at what the text says.
2. Enclose your guess in square brackets with a question mark, like this: [unclear word?]
3. If you have multiple guesses, separate them with a comma inside the brackets, like this: [unclear word1?, unclear word2?]
4. If a word or phrase is completely illegible, use [illegible] as a placeholder.

Once you have completed the transcription, provide your output within <transcription> tags. Begin
your transcription immediately without any preamble or explanation. Ensure that your transcription accurately 
reflects the content and structure of the original document.
'''
    test_data = extract_json('documents/NARA_chosen.json')
    
    model = sys.argv[1].lower()

    # If document number is specified then transcribe only that document
    if (len(sys.argv) > 2):
        id = sys.argv[2]
        data = test_data.get('digitalObjects', [])
        for d in data:
            file = d.get('objectUrl').rsplit('/', 1)[-1].split('.')[0]
            if (file == id or d.get('objectId') == id):
                transcribe_docs(d, prompt, gpt, claude, model)
                return
        print("Document not found")
        return
    
    # Transcribe all documents
    for data in test_data.get('digitalObjects', []):
        transcribe_docs(data, prompt, gpt, claude, model)   
        

if __name__ == "__main__":
    main()