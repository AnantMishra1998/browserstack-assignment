import os
import threading
from test_scraper import scrape_opinion_articles
from translator import translate_titles
from analyzer import analyze_repeats
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
load_dotenv()


BROWSERSTACK_USERNAME = os.getenv("BROWSERSTACK_USERNAME")
BROWSERSTACK_ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")

def run_browserstack_test(browser_name, os_name, os_version, options_class):
    print(f"Starting test: {browser_name} on {os_name} {os_version}")

    options = options_class()
    options.set_capability('browserName', browser_name)
    options.set_capability('os', os_name)
    options.set_capability('osVersion', os_version)
    options.set_capability('name', f"BrowserStack Test - {browser_name} on {os_name}")
    options.set_capability('build', 'BStack Build #1')
    options.set_capability('browserstack.debug', True)

    remote_url = f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub.browserstack.com/wd/hub"
    
    try:
        driver = webdriver.Remote(command_executor=remote_url, options=options)
        titles = scrape_opinion_articles(driver)
        translated = translate_titles(titles)

        print("\nTranslated Titles:")
        for t in translated:
            print(f"- {t}")

        analyze_repeats(translated)

    except Exception as e:
        print(f"[ERROR] {browser_name} {os_name} Test failed:", e)
    finally:
        try:
            driver.quit()
        except:
            pass

test_configs = [
    ("Chrome", "Windows", "11", ChromeOptions),
    ("Firefox", "OS X", "Ventura", FirefoxOptions),
    ("Edge", "Windows", "10", EdgeOptions),
    ("iPhone 13", "iOS", "15", ChromeOptions), 
    ("Samsung Galaxy S22", "android", "12.0", ChromeOptions),
]

if __name__ == "__main__":
    print("Starting parallel execution on BrowserStack...")

    threads = []
    for config in test_configs:
        t = threading.Thread(target=run_browserstack_test, args=config)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("All tests completed.")