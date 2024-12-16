import requests
from dotenv import load_dotenv
import json
import os
load_dotenv()
GEMINI_API_TOKEN = os.getenv("GEMINI_API_TOKEN")
GEMINI_PROMPT_URL = os.getenv("GEMINI_API_URL") + "=" + GEMINI_API_TOKEN

# data must be JSON and follows the format {candidates : [{content : {parts: [{text}]}}]
def clean_api_data(data):
    try :
        cleaned_data = data['candidates'][0]['content']['parts'][0]['text'].replace("```json","").replace("```","")
        start_index = cleaned_data.find('[')
        end_index = cleaned_data.find(']')
        if start_index != -1 and end_index != -1:
            cleaned_data = json.loads(cleaned_data[start_index:end_index+1])
        return cleaned_data
    except Exception as e:
        print("Error during cleaning returned Data: ", e)
        return None

def query_gemini_api(prompt):
    payload = {'contents': [{'parts': [{'text': prompt}]}]}
    try:
        response = requests.post(GEMINI_PROMPT_URL, headers={"Content-Type": "application/json"}, json=payload)
        response.raise_for_status()
        data =clean_api_data(response.json())
        return data  
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
        return None
    except Exception as e:
        print("An unexpected error occurred:", e)
        return None
    
# fully functional, looks for recommendations through gemini api
# @returns array of recommendations format : {name: name, actual_price: price, desc: description}
def get_recommendations(product, budget):
    # sanitizing the prompt
    sanitize_request = f"answer with only hardware or software but not both or no, is {product} related to technology or gaming ?"
    type = query_gemini_api(sanitize_request).strip().lower()
    print (type)
    if type == "no":
        return [], "Not allowed"
    elif type == "software" or type == "hardware":
        # creating the prompt
        prompt = f"""Provide a JSON array of {product} recommendations within a ${budget} budget. 
        The JSON format should contain the fields: "name" (with brand), "actual_price", and "desc". No extra text."""
        recommendations = query_gemini_api(prompt)
        return recommendations, type
    else :
        raise Exception("Unexpected response from API")

# processing the recommendations and adding in the links necessary
def finalizing_recommendations(product,budget):
    recommendations , type = get_recommendations(product,budget)
    if  type == "Not allowed":
        return ("Only Tech related recommendations are allowed")
    if type == "software":
        for recommendation in recommendations:
            name = recommendation["name"].replace(" ","%20")
            recommendation["links"] = [
                f"https://www.eneba.com/store/all?text={name}",
                f"https://www.amazon.com/s?k={name}",
                f"https://www.instant-gaming.com/en/search/?query={name}",
                f"https://store.steampowered.com/search/?term={name}"
                f"https://www.epicgames.com/store/en-US/search?search={name}"
                f"https://allgoodkeys.com/?s={name}"
            ]
        
    if type == "hardware":
        for recommendation in recommendations:
            name = recommendation["name"].replace(" ","%20")
            recommendation["links"] = [
                f"https://www.amazon.com/s?k={name}",
                f"https://www.ultrapc.ma/recherche?controller=search&s={name}",
                f"https://www.ebay.com/sch/i.html?&_nkw={name}",
                f"https://www.aliexpress.com/w/wholesale-{name}.html"
            ]    
    #for testing uncomment this
    # with open("src/GamingFunctionality/recommendations.json", "w") as f:
    #     json.dump(recommendations, f)
    return recommendations
        
# finalizing_recommendations("PS5",1000)