from deep_translator import GoogleTranslator
from find_description import find_similar_descriptions
from similaritycheck import compare_descriptions

def translate_japanese_to_english(text):
    return GoogleTranslator(source='ja', target='en').translate(text)

def comparative_analysis(cve_data):
    cve_id = cve_data.get("id", "Unknown CVE")
    description = cve_data.get("description", "No description available")
    base_score = cve_data.get("cvss_v2", {}).get("baseScore", 0)
    access_complexity = cve_data.get("cvss_v2", {}).get("accessComplexity", "UNKNOWN")
    translated_description = translate_japanese_to_english(description)
    results = find_similar_descriptions(translated_description)
    if results:
        for result in results:
            d1 = result.get("description", "No description available")
            d2 = translated_description
            similarity = compare_descriptions(d1,d2)
            if similarity > 0.7: 
               return result.get("id")
    else:
        print("No similarity found")       
        return "";    
                
        

