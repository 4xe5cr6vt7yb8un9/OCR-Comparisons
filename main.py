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
    prompt = "Please transcribe the text from the following image with high accuracy. Ensure that all punctuation, capitalization, and formatting are preserved as closely as possible to the original. If any part of the text is illegible or unclear, indicate this with '[illegible]' in the transcription. Pay special attention to names, dates, and any specific terminology. Please provide only the transcription."
    prompt2 = '''
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

If you encounter any partsof the text that are unclear or difficult to read:
1. Make your best guess at what the text says.
2. Enclose your guess in square brackets with a question mark, like this: [unclear word?]
3. If a word or phrase is completely illegible, use [illegible] as a placeholder.

Once you have completed the transcription, present your final output within <transcript> tags.
Ensure that your transcription accurately reflects the content and structure of the original
document.

<example>
<document> https://s3.amazonaws.com/NARAprodstorage/opastorage/live/39/9317/54931739/content/23_b/M804-RevolutionaryWarPensionAppFiles_b/M804_1336/images/4159578_00897.jpg </document>
<transcript> Declaration\nIn order to obtain the benefits of the Acts of Congress 15th May 1828 7th July 1838\nState of New York\nOneida County:\nOn this 21st day of October in the year of our Lord One thousand eight hundred and fifty two, personally appeared before the Honorable Ralph McIntosh Special Surrogate and Justice of a Court of Record in and for the County of Oneida and State of New York aforesaid Mary House aged eighty 80 years, a resident of Oneida in the County of Oneida, who being duly sworn according to law, doth upon her oath makes the following declaration in order to obtain she benefits of the provisions made by the Act of Congress passed 15th May 1828 entitled Pension granted to all the officers who served to the end of the Revolutionary War in the Continental Army also the Act of Congress passed July 7th 1838 entitled an Act granting half pay and pensions to certain widow and the other acts of Congress extending said act that she is the widow of John House deceased who was a private in the Revolutionary War in Company Commanded first by Captain Andrew Frink and afterwords and near the later part of said war by Captain Sytez in the first Military Regiment of the original Five Regiments of the New York troops in the Continental Line Commanded by Colonel Goose Van Schaicks, that he enlisted some time in about the month of January or February in the year of our lord seventeen </transcript>
</example>
'''
    test_data = extract_json('testing_data.json')
    
    model = sys.argv[1].lower()

    # If document number is specified then transcribe only that document
    if (len(sys.argv) > 2):
        num = int(sys.argv[2])
        data = test_data.get('data', [])[num]
        transcribe_docs(data, prompt2, gpt, claude, model)
        return
    
    # Transcribe all documents
    for data in test_data.get('data', []):
        transcribe_docs(data, prompt, gpt, claude, model)   
        

if __name__ == "__main__":
    main()