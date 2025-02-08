import asyncio
import json
from googletrans import Translator
from langdetect import detect

translator = Translator()
async def translate_text(text, src_lang):
    try:
        translated_text = await translator.translate(text, src=src_lang, dest="en")
        return translated_text.text
    except Exception as e:
        print(f"Translation failed: {e}")
        return text

async def translate_descriptions():
    with open("binlog_events.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    tasks = []
    descriptions = []
    for row in data:
        row_data = row.get("data", {})
        description = row_data.get("description", "")
        if not description:
            continue
        try:
            language_code = detect(description)
        except:
            language_code = "unknown"
        if language_code != "en":
            tasks.append(translate_text(description, language_code))
            descriptions.append(row_data)
    translations = await asyncio.gather(*tasks)
    for desc, translated_text in zip(descriptions, translations):
        desc["description"] = translated_text
    with open("binlog_events_translated.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

asyncio.run(translate_descriptions())