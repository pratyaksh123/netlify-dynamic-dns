import requests
import json
import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()

NETLIFY_AUTH_TOKEN = os.getenv('NETLIFY_AUTH_TOKEN')
NETLIFY_DNS_ZONE_ID = os.getenv('NETLIFY_DNS_ZONE_ID')

def get_external_ip():
    response = requests.get("http://checkip.amazonaws.com/")
    if response.status_code == 200:
        return response.text.strip()
    else:
        logging.error(f"Failed to fetch external IP: {response.status_code}, {response.text}")
        return None

def get_dns_zones():
    url = "https://api.netlify.com/api/v1/dns_zones"
    headers = {'Authorization': f'Bearer {NETLIFY_AUTH_TOKEN}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"Failed to fetch DNS zones: {response.status_code}, {response.text}")
        return None

def get_dns_records():
    url = f"https://api.netlify.com/api/v1/dns_zones/{NETLIFY_DNS_ZONE_ID}/dns_records"
    headers = {'Authorization': f'Bearer {NETLIFY_AUTH_TOKEN}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"Failed to fetch DNS records: {response.status_code}, {response.text}")
        return None

def delete_dns_record(record_id):
    url = f"https://api.netlify.com/api/v1/dns_zones/{NETLIFY_DNS_ZONE_ID}/dns_records/{record_id}"
    headers = {'Authorization': f'Bearer {NETLIFY_AUTH_TOKEN}'}
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        logging.info("DNS record deleted successfully")
        return True
    else:
        logging.error(f"Failed to delete DNS record: {response.status_code}, {response.text}")
        return False

def create_dns_record(hostname, value):
    url = f"https://api.netlify.com/api/v1/dns_zones/{NETLIFY_DNS_ZONE_ID}/dns_records"
    payload = json.dumps({
        "type": "A",
        "hostname": hostname,
        "value": value,
        "ttl": 300
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {NETLIFY_AUTH_TOKEN}'
    }
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 201:
        logging.info("DNS record created successfully")
        return True
    else:
        logging.error(f"Failed to create DNS record: {response.status_code}, {response.text}")
        return False

if __name__ == "__main__":
    desired_ip = get_external_ip()
    if desired_ip:
        records = get_dns_records()
        if records:
            for record in records:
                if record['hostname'] == "vpn.pratyaksh.me" and record['type'] == "A":
                    if record['value'] != desired_ip:
                        logging.info(f"DNS record needs update: Current IP {record['value']} vs External IP {desired_ip}")
                        if delete_dns_record(record['id']):
                            create_dns_record("vpn.pratyaksh.me", desired_ip)
                    else:
                        logging.info("No update needed, DNS record is correct")
    else:
        logging.error("Could not obtain the external IP")
