import fastapi
import requests
import json
from pydantic import BaseModel
from dotenv import load_dotenv
import os

"""
    Environment Variables
"""
load_dotenv()
IPDB_API_KEY= os.environ["AIPDB_API_TOKEN"]


"""
    Defining API Endpoints
"""

class Attack(BaseModel):
    origin_ip: str
    origin_con: str
    dest_con: str

# Gets the latest reported IPs by abuseIPDB
def get_blacklist_ips():
    url = "https://api.abuseipdb.com/api/v2/blacklist"
    quertystring = {
        'limit': '10000',
    }

    headers = {
        'Accept': 'text/plain',
        'key': IPDB_API_KEY,
    }

    response = requests.request(method='GET', url=url, headers=headers, params=quertystring)
    res= response.text.split("\n")
    print(res)
    return res 

def create_attack_list():
    ips= ["112.27.102.137"] #get_blacklist_ips()
    url = "https://api.abuseipdb.com/api/v2/check"
    reports_url = "https://api.abuseipdb.com/api/v2/reports"
    for ip in ips:
        quertystring = {
            'ipAddress': ip,
            'maxAgeInDays': 90,
        }

        headers = {
            'Accept': 'application/json',
            'Key': IPDB_API_KEY,
        }

        response = requests.request(method='GET', url=url, headers=headers, params=quertystring)
        reports = requests.request(method='GET', url=reports_url, headers=headers, params=quertystring)
        decodedResponse = json.loads(response.text)
        decodedReports = json.loads(reports.text)
        print(ip + decodedResponse["data"]["countryCode"] + str(decodedReports["data"]["results"]))

create_attack_list()