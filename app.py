import fastapi
import requests
import json
from pydantic import BaseModel
from dotenv import load_dotenv
import os, io

"""
    Environment Variables
"""
load_dotenv()
IPDB_API_KEY= os.environ["AIPDB_API_TOKEN"]
CLOUDFLARE_API_KEY= os.environ["CF_API_TOKEN"]
MODE = os.environ["MODE"]
CF_API_URL= "https://api.cloudflare.com/client/v4"
PARAMS= "dateRange=7d&format=csv"

"""
    Defining API Endpoints
"""

headers = {
    "Authorization": f"Bearer {CLOUDFLARE_API_KEY}"
}
r = requests.get(f"{CLOUDFLARE_API_KEY}/radar/http/summary/device_type?{PARAMS}",
                 headers=headers)
df = pd.read_csv(io.StringIO(r.text))
df.plot(kind="bar", stacked=True)



