import requests
import xml.etree.ElementTree as ET
import json
import time
from datetime import datetime


BASE_URL = "https://jvndb.jvn.jp/myjvn"
today_date = datetime.now().strftime("%Y-%m-%d")


NAMESPACES = {
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rss": "http://purl.org/rss/1.0/",
    "jvn": "http://jvndb.jvn.jp/rss/"
}


def fetch_all_vulnerabilities():
    all_vulnerabilities = []
    start_item = 1
    batch_size = 100 

    while True:
        params = {
            'method': 'getVulnOverviewList',
            'feed': 'hnd',  
            'startItem': start_item,
            'maxCount': batch_size,  
            'datePublished': today_date
        }

        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()

            
            root = ET.fromstring(response.text)

          
            vulnerabilities = []
            for item in root.findall(".//rss:item", NAMESPACES):
                vuln_data = {"db": "jvn"}

    
                identifier = item.find(".//jvn:identifier", NAMESPACES)
                vuln_data["cveid"] = identifier.text if identifier is not None else "N/A"

   
                for child in item:
                    tag = child.tag.split("}")[-1]  
                    vuln_data[tag] = child.text if child.text else "N/A"

                vulnerabilities.append(vuln_data)

            if not vulnerabilities:
                break  

            all_vulnerabilities.extend(vulnerabilities)
            start_item += batch_size  

            print(f"Fetched {len(vulnerabilities)} vulnerabilities, total: {len(all_vulnerabilities)}")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            break

    return all_vulnerabilities


def save_to_json(data, filename="jvn_data.json"):
    with open(filename, "w", encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def jvn():
    while True:
        print("\nFetching all vulnerabilities from JVN...")
        vuln_data = fetch_all_vulnerabilities()
        if vuln_data:
            save_to_json(vuln_data)
            print(f"Data saved to jvn_data.json")
        else:
            print("No new data fetched.")
        print("\nWaiting for the next daily update...\n")
        time.sleep(86400)  
