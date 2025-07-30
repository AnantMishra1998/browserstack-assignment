# translator.py

import requests
import time

def translate_titles(titles):
    translated = []
    for title in titles:
        try:
            url = "https://translate.googleapis.com/translate_a/single"
            params = {
                "client": "gtx",
                "sl": "es",   # Source language: Spanish
                "tl": "en",   # Target language: English
                "dt": "t",
                "q": title
            }

            response = requests.get(url, params=params)
            result = response.json()
            translated_text = result[0][0][0]

            translated.append(translated_text)
            time.sleep(1)  # polite delay to avoid rate limit

        except Exception as e:
            print(f"⚠️ Translation failed for: {title}\nError: {e}")
            translated.append("[Translation failed]")

    return translated
