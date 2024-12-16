import requests
from dotenv import load_dotenv
import json
import os
load_dotenv()
GEMINI_API_TOKEN = os.getenv("GEMINI_API_TOKEN")
GEMINI_PROMPT_URL = os.getenv("GEMINI_API_URL") + "=" + GEMINI_API_TOKEN

def get_recommendations(product, budget):
    prompt = f"""for further processing through my api, Give the result only of recommendations of {product} I could buy in budget of {budget}$ (dollars), 
    the output should be only in json format containing [name(with brand) , actual price,desc] with no additional information or notes."""

    payload = {'contents': [{'parts': [{'text': prompt}]}]}
    
    try:
        response = requests.post(GEMINI_PROMPT_URL, headers={"Content-Type": "application/json"}, json=payload)
        response.raise_for_status()
        content = response.json()
        cleaned_data = json.loads(content['candidates'][0]['content']['parts'][0]['text'].replace("```json","").replace("```",""))
        for product in cleaned_data :
            print(product)
        return cleaned_data  
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
        return None
