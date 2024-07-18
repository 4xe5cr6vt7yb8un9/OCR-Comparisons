import requests
import json
from os.path import exists


def extract_digital_objects(naID):
    # URL for object metadata
    url = f"https://catalog.archives.gov/proxy/records/search?naId_is={naID}&allowLegacyOrgNames=true&includeExtractedText=true"
    # URL for object transcript
    url2 = f"https://catalog.archives.gov/proxy/contributions/targetNaId/{naID}"

    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9"    
    }

    response = requests.get(url, headers=headers)
    response2 = requests.get(url2, headers=headers)
    
    if response.status_code == 200 and response2.status_code == 200:
        data = response.json()
        transcript_data = response2.json()

        # There is a lot more data in this JSON object I am just including the dict that has the specific file details.
        digital_objects = data["body"]["hits"]["hits"][0]["_source"]["record"]["digitalObjects"]
        start_date = data["body"]["hits"]["hits"][0]["_source"]["record"]["ancestors"][1]["inclusiveStartDate"]["year"]
        end_date = data["body"]["hits"]["hits"][0]["_source"]["record"]["ancestors"][1]["inclusiveEndDate"]["year"]
        extracted_objects = []

        for obj in digital_objects:
            id = obj["objectId"]
            extract = ""
            for contrib in transcript_data:
                if contrib["targetObjectId"] == id and contrib["contributionType"] == "transcription":
                    extract = contrib["contribution"]
                    break

            if extract == "":
                continue

            extracted_obj = {
                "objectId": obj["objectId"],
                "date_range": f"{start_date}-{end_date}",
                "objectUrl": obj["objectUrl"],
                "extractedText": extract,
                "objectDescription": obj["objectDescription"],
                # ... (Include any other fields you want to extract)
            }
            extracted_objects.append(extracted_obj)

        # Specifies where to save output
        output_file = f"documents/NARA_files.json"
            
        # If the output file exists then append the data else create a new file
        if not exists(output_file):
            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump({"digitalObjects": extracted_objects}, file, indent = 4, ensure_ascii=False)
        else:
            with open(output_file, 'r+', encoding='utf-8') as file:
                # Appends data to the output file
                file_data = json.load(file)
                for obj in extracted_objects:
                    file_data["digitalObjects"].append(obj)
                file.seek(0)
                json.dump(file_data, file, indent = 4, ensure_ascii=False)

    else:
        return json.dumps({"error": f"Request failed with status code: {response.status_code}"})

if __name__ == '__main__':
    # Pass in the NAID
    id = input("Enter the NAID: ")
    ext = extract_digital_objects(naID=54953855)

    