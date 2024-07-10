import requests
import json

def extract_digital_objects(naID):
    url = f"https://catalog.archives.gov/proxy/records/search?naId_is={naID}&allowLegacyOrgNames=true&includeExtractedText=true"

    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9"    
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()

        # There is a lot more data in this JSON object I am just including the dict that has the specific file details.
        digital_objects = data["body"]["hits"]["hits"][0]["_source"]["record"]["digitalObjects"]
        extracted_objects = []

        for obj in digital_objects:
            extracted_obj = {
                "objectId": obj["objectId"],
                "objectUrl": obj["objectUrl"],
                "extractedText": obj["extractedText"],
                "objectDescription": obj["objectDescription"],
                # ... (Include any other fields you want to extract)
            }
            extracted_objects.append(extracted_obj)

        return json.dumps({"digitalObjects": extracted_objects})  # Return as JSON string
    else:
        return json.dumps({"error": f"Request failed with status code: {response.status_code}"})

if __name__ == '__main__':
    # Pass in the NAID
    print(extract_digital_objects(naID=54953855))