import requests
import time
import json
from datetime import datetime, timedelta


API_KEY = "09402102-19ae-451c-a77a-1ca08df74664"  

BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

def fetch_todays_cves():
    headers = {"apiKey": API_KEY} if API_KEY else {}
    today = datetime.utcnow().date().isoformat()
    params = {
        "pubStartDate": f"{today}T00:00:00.000",
        "pubEndDate": f"{today}T23:59:59.999",
        "resultsPerPage": 2000,  
        "startIndex": 0,
    }
    
    cve_list = []
    try:
        while True:
            response = requests.get(BASE_URL, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            for cve in data.get("vulnerabilities", []):
                cve_data = cve.get("cve", {})
                cve_entry = {
                    "db": "usnvd",
                    "id": cve_data.get("id"),
                    "description": cve_data.get("descriptions", [{}])[0].get("value", "No description"),
                    "published": cve_data.get("published"),
                    "modified": cve_data.get("lastModified"),
                    "source_identifier": cve_data.get("sourceIdentifier"),
                    "cvss_v3": cve_data.get("metrics", {}).get("cvssMetricV31", [{}])[0].get("cvssData", {}),
                    "cvss_v2": cve_data.get("metrics", {}).get("cvssMetricV2", [{}])[0].get("cvssData", {}),
                    "impact": cve_data.get("impact", {}),
                    "references": cve_data.get("references", []),
                    "configurations": cve_data.get("configurations", {}),
                }
                cve_list.append(cve_entry)
            
       
            total_results = data.get("totalResults", 0)
            if params["startIndex"] + params["resultsPerPage"] >= total_results:
                break
            
            params["startIndex"] += params["resultsPerPage"]
            time.sleep(1)  
        
        return cve_list
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

def save_to_json(cve_data, filename="cve_today.json"):
    with open(filename, "w") as json_file:
        json.dump(cve_data, json_file, indent=4)

def usnvd():
    print("\nFetching today's vulnerabilities from NVD...")
    cve_data = fetch_todays_cves()
    if cve_data:
        save_to_json(cve_data)
        print(f"Data saved to cve_today.json")
    else:
        print("No new CVEs found for today.")
