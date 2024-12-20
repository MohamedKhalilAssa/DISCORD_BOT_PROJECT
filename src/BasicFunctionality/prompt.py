import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_TOKEN = os.getenv("GEMINI_API_TOKEN")


genai.configure(api_key=GEMINI_API_TOKEN)
model = genai.GenerativeModel("gemini-1.5-flash")


def result(prompt):
    response = model.generate_content(prompt) 
    candidates = response.candidates  
    if candidates:
        
        generated_text = candidates[0].content.parts[0].text
        return generated_text
    else:
        return "No response generated."
    

async def contain_bad_words(message):
    res = result(f"answer with Yes or NO, does{message} contain any bad word in context of racism, religion,... etc")
    output = res.lower().strip().replace("." , "")
    print(output)
    if output == "yes":
        return True
    elif output == "no":     # use try except
        return False
    else :
        print("Unexpected response:", output)
        return False
    
