from utils import log_transcription, extract_json
from compare import word_distance

from langchain_community.llms import Ollama

test_data = extract_json('testing_data.json')

llm = Ollama(model='mixtral')

for data in test_data.get('data', []):
    url = data.get('image_url')

    print(f"Transcribing image: {url}")
    prompt = f"Please transcribe the text from the following image with high accuracy. Ensure that all punctuation, capitalization, and formatting are preserved as closely as possible to the original. If any part of the text is illegible or unclear, indicate this with '[illegible]' in the transcription. Pay special attention to names, dates, and any specific terminology. Please provide only the transcription: {url}"
    response = llm.invoke(prompt)
    print("Finished transcription")

    # Calculates the distance between the automatted and manual transcriptions
    print("Calculating word distance")
    manual_text = data.get("image_text")
    distance = word_distance([response, manual_text])
    print('The transcription has a distance of %.4F\n' % distance)

    log_transcription(response, "Mixtral", distance, prompt, url)