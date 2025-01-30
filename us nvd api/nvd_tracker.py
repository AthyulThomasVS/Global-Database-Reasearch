import requests
import time
import json

# Your NVD API Key (Optional but recommended)
API_KEY = "09402102-19ae-451c-a77a-1ca08df74664"  # Replace with your API key

# NVD API Endpoint
BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

# Function to fetch latest CVEs and store in an array
def fetch_latest_cves():
    headers = {"apiKey": API_KEY} if API_KEY else {}
    params = {
        "resultsPerPage": 10,  # Fetch 5 latest vulnerabilities
        "startIndex": 0,
    }

    cve_list = []  # Array to store CVE data
    
    try:
        response = requests.get(BASE_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        # Extract and store CVE details
        for cve in data.get("vulnerabilities", []):
            cve_data = cve.get("cve", {})
            cve_entry = {
                "id": cve_data.get("id"),
                "description": cve_data.get("descriptions", [{}])[0].get("value", "No description"),
                "published": cve_data.get("published"),
                "severity": cve_data.get("metrics", {}).get("cvssMetricV31", [{}])[0].get("cvssData", {}).get("baseSeverity", "Unknown")
            }
            cve_list.append(cve_entry)

        return cve_list
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

# Function to save CVE data to a JSON file
def save_to_json(cve_data, filename="cve_data.json"):
    with open(filename, "w") as json_file:
        json.dump(cve_data, json_file, indent=4)

# Continuous monitoring (runs every 1 hour)
if __name__ == "__main__":
    while True:
        print("\nFetching latest vulnerabilities from NVD...")
        cve_data = fetch_latest_cves()
        if cve_data:
            save_to_json(cve_data)
            print(f"Data saved to cve_data.json")
        print("\nWaiting for the next update...\n")
        time.sleep(3600)  # Wait for 1 hour before the next check
