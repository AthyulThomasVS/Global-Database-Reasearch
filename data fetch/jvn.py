import requests
import xml.etree.ElementTree as ET
import json
import time

# JVN API Endpoint
BASE_URL = "https://jvndb.jvn.jp/myjvn"

# Define XML namespaces
NAMESPACES = {
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rss": "http://purl.org/rss/1.0/",
    "jvn": "http://jvndb.jvn.jp/rss/"
}

# Function to fetch and parse vulnerabilities
def fetch_latest_vulnerabilities():
    params = {
        'method': 'getVulnOverviewList',
        'feed': 'hnd',  
        'startItem': 1,
        'maxCount': 10,  # Increased count to fetch more data
        'datePublished': '2025-01-01'
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()

        # Print the raw XML response for debugging
        print("Raw XML Response:", response.text[:500])  # Print first 500 chars

        # Parse XML response with namespaces
        root = ET.fromstring(response.text)

        # Find all <item> elements in the XML
        vulnerabilities = []
        for item in root.findall(".//rss:item", NAMESPACES):
            vuln_data = {}

            # Look for an identifier field in the item element
          
            identifier = item.find(".//jvn:identifier", NAMESPACES)  # Try to find identifier

            if identifier is not None:
                vuln_data["cveid"] = identifier.text
            else:
                # Fallback if not found
                vuln_data["cveid"] = "N/A"

            # Loop through each child element in item to get other fields
            vuln_data["db"] = "jvn"
            for child in item:
                tag = child.tag.split("}")[-1]  # Remove namespace

                # Add the other fields to the vuln_data
                vuln_data[tag] = child.text if child.text else "N/A"

            vulnerabilities.append(vuln_data)

        return vulnerabilities

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

# Function to save data to JSON file
def save_to_json(data, filename="dummyab.json"):
    with open(filename, "w", encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    while True:
        print("\nFetching latest vulnerabilities from JVN...")
        vuln_data = fetch_latest_vulnerabilities()
        if vuln_data:
            save_to_json(vuln_data)
            print(f"Data saved to dummyss.json")
        else:
            print("No new data fetched.")
        print("\nWaiting for the next update...\n")
        time.sleep(3600)  # Wait 1 hour before the next fetch