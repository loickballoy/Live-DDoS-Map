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
MODE = os.environ["MODE"]


"""
    Defining API Endpoints
"""

class Attack(BaseModel):
    origin_ip: str
    origin_con: str
    dest_con: str
    att_time: str

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
    print(response.text)
    return res 

def create_attack_list():
    ips = []
    if MODE != "DEV":   
        ips= get_blacklist_ips()
    else:
        with open('test_ip.txt') as f:
            ips = f.read().splitlines()
    url = "https://api.abuseipdb.com/api/v2/check"
    reports_url = "https://api.abuseipdb.com/api/v2/reports"
    Attack_List = []
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
        for report in decodedReports["data"]["results"]:
            print(ip + "\n" + decodedResponse["data"]["countryCode"] + "\n" + report["reporterCountryCode"] + 
                                                                              "\n" + report["reportedAt"] + "\n\n")
            Attack_List.append(Attack(
                origin_ip= ip,
                origin_con= decodedResponse["data"]["countryCode"],
                dest_con= report["reporterCountryCode"],
                att_time= report["reportedAt"]
            ))
 
create_attack_list()
