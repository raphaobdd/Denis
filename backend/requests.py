import requests
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="C:/Canguru/Denis/.env")

url = os.getenv("API_URL")

print(url)