import requests
from dotenv import load_dotenv
import json
import os
# SECOND PART: for the deals and maybe free games that would be scraped from some website
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

load_dotenv()
GEMINI_API_TOKEN = os.getenv("GEMINI_API_TOKEN")
GEMINI_PROMPT_URL = os.getenv("GEMINI_API_URL") + "=" + GEMINI_API_TOKEN
# FIRST PART: for the buy functionality and recommendations.  

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
        print("A request error has occurred:", e)
        return None
    except Exception as e:
        print("An unexpected error occurred:", e)
        return None
    
# fully functional, looks for recommendations through gemini api
def get_recommendations(product, budget):
    # sanitizing the prompt
    sanitize_request = f"answer with only one of the following options (No | hardware | Software), if {product} is related to electronics,technology or gaming ?"
    type = query_gemini_api(sanitize_request).strip().lower().replace(".","")
    print(type)
    if type == "no":
        return [], "Not allowed"
    elif type == "software" or type == "hardware":
        # creating the prompt
        prompt = f"""Provide a JSON array of {product} recommendations (up to 5) within a ${budget} budget. 
        The JSON format should contain the fields: "name" (with brand), "actual_price", and "desc". No extra text."""
        recommendations = query_gemini_api(prompt)
        return recommendations, type
    else :
        raise Exception("Unexpected response from API")

# @returns array of recommendations format : {name: name, actual_price: price, desc: description}
# processing the recommendations and adding in the links necessary
def finalizing_recommendations(product,budget):
    recommendations , type = get_recommendations(product,budget)
    if  type == "Not allowed":
        return -1, ("Only Tech related recommendations are allowed")
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
    return 1, recommendations
        
# finalizing_recommendations("PS5",1000)

# SECOND PART: for the deals and maybe free games that would be scraped from some website
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

#@return format: [{name,deal_value,old_value, image, link}...] 
def scrape_deals(max_deals=10):
    driver = webdriver.Chrome() 
    websitelink = "https://gg.deals"
    driver.get(f"{websitelink}/deals/") # navigate to the website
    WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME, "deal-list-item")))
    elements = BeautifulSoup(driver.page_source, "html.parser").find_all("div", class_="deal-list-item", limit=max_deals)
    driver.quit()
    deals = []
    for element in elements :
        # scrapping the image
        try :
            image = element.select_one(".game-image .main-image picture img")
            image = image['srcset'].split(',')[1].replace(" 2x", "") or image['src']
            #Deal Value and name
            deal_value = element.select_one(".price-wrapper .game-price-new").text 
            old_value = element.select_one("span.price-label.price-old")
            if old_value is not None:
                old_value = old_value.text
            else:
                old_value = "..."
            game_name = element.select_one(".game-info-wrapper .game-info-title-wrapper .title").text   
            #deal link
            deal_link = websitelink + element.select_one(".game-cta .shop-link")['href']
            deals.append({
                "name": game_name,
                "deal_value": deal_value,
                "old_value": old_value,
                "image": image,
                "link": deal_link
            })
        except Exception as e:
            print("Error during scrapping deals: ", e)
            continue
    
    return deals
