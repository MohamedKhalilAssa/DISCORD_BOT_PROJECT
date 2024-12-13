import requests
from dotenv import load_dotenv
import os
load_dotenv()
TOKEN = os.getenv('API_TOKEN') 
headers = { 'X-Auth-Token': TOKEN }


