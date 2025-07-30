import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# tests/test_scraper.py
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from translator import translate_titles
from analyzer import analyze_repeats

def scrape_opinion_articles(driver):
    print("Script started...\n")
    titles = []

    driver.get("https://elpais.com/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    print("Opened El País")

    try:
        accept_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button"))
        )
        accept_btn.click()
        print("Accepted cookies")
    except:
        print("No cookie popup found or already dismissed")

    try:
        opinion_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Opinión"))
        )
        opinion_link.click()
        print("Opened Opinión section")
    except Exception as e:
        print("Failed to open Opinión section:", e)
        return titles

    for i in range(5):
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//article")))
            articles = driver.find_elements(By.XPATH, "//article")
            if i >= len(articles):
                print(f"Only found {len(articles)} articles.")
                break

            article = articles[i]
            title_elem = article.find_element(By.XPATH, ".//h2")
            title = title_elem.text.strip()
            titles.append(title)
            print(f"\nTitle {i+1} (Spanish): {title}")

            article_url = article.find_element(By.TAG_NAME, "a").get_attribute("href")
            driver.get(article_url)

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            # Try multiple possible content containers
            # Scrape article content
            try:
                selectors = ["article p.c_d", "article p.a_st", "article h2.a_st", "article p"]
                content_parts = []
                for sel in selectors:
                    content_parts += [p.text.strip() for p in driver.find_elements(By.CSS_SELECTOR, sel) if p.text.strip()]
                content = "\n".join(dict.fromkeys(content_parts))  # Remove duplicate lines
                if not content:
                    content = "Unable to scrape content...."
            except Exception as e:
                content = f"Error scraping content: {e}"

            print(f"Content {i + 1} (Spanish): {content[:200]}...")

            try:
                img = driver.find_element(By.XPATH, "//figure//img")
                img_url = img.get_attribute("src")
                os.makedirs("images", exist_ok=True)
                with open(f"images/article_{i+1}.jpg", "wb") as f:
                    f.write(requests.get(img_url).content)
                print("Image downloaded.")
            except:
                print("No image found.")

            # Go back and re-fetch articles
            driver.back()

        except Exception as e:
            print(f"Error scraping article {i+1}: {e}")
            continue

    print(f"\nScraped {len(titles)} article titles.\n")
    return titles

# ---- Run Script ----
if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")  # Hide browser
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()

    try:
        titles = scrape_opinion_articles(driver)
        translated = translate_titles(titles)

        print("\nTranslated Titles:")
        for t in translated:
            print(f"- {t}")

        print()
        analyze_repeats(translated)

    finally:
        driver.quit()
        print("\nDriver closed.")
