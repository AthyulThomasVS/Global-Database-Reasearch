import matplotlib.pyplot as plt
import json

def datachart(cve_data):
    # json_file_path = r"C:/Users/abdul/OneDrive/Desktop/Global-Database-Reasearch/cve_data.json"
    # with open(json_file_path, "r", encoding="utf-8") as file:
    #     cve_list = json.load(file)  

    # cve_data = cve_list[0]  # Access the first CVE entry

    # Extract data safely
    cve_id = cve_data.get("id", "Unknown CVE")
    description = cve_data.get("description", "No description available")
    base_score = cve_data.get("cvss_v2", {}).get("baseScore", 0)
    access_complexity = cve_data.get("cvss_v2", {}).get("accessComplexity", "UNKNOWN")

    # Assign numerical values to access complexity levels
    complexity_comparison = {"LOW": 1, "MEDIUM": 2, "HIGH": 3}
    access_complexity_value = complexity_comparison.get(access_complexity, 0)

    # Create a figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))

    # Plot 1: Base Score Visualization
    ax1.bar(["baseScore"], [base_score], color='blue')
    ax1.set_title(f"Base Score for {cve_id}")
    ax1.set_ylim(0, 10)
    ax1.set_ylabel("Score (out of 10)")
    ax1.text(0, min(base_score + 0.5, 9.5), f"{base_score}", ha='center', fontsize=12)

    # Plot 2: Access Complexity Visualization
    colors = {'LOW': 'green', 'MEDIUM': 'orange', 'HIGH': 'red'}
    ax2.bar(["LOW", "MEDIUM", "HIGH"], 
            [1 if access_complexity == level else 0 for level in ["LOW", "MEDIUM", "HIGH"]], 
            color=[colors[level] for level in ["LOW", "MEDIUM", "HIGH"]])

    ax2.set_title(f"Access Complexity for {cve_id}")
    ax2.set_ylabel("Presence (1: Present, 0: Not Present)")

    # Display the CVE description
    fig.suptitle(f"{cve_id}: {description}", fontsize=14, fontweight='bold')

    # Adjust layout and show plot
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()
