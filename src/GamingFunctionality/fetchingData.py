import requests
from dotenv import load_dotenv
import os
load_dotenv()
TOKEN = os.getenv('API_TOKEN') 
headers = { 'X-Auth-Token': TOKEN }



uri = 'https://api.football-data.org/v4/matches'

response = requests.get(uri, headers=headers)
for match in response.json()['matches']:
  print(match)