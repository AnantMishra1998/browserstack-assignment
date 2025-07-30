# El País Opinion Scraper – BrowserStack Automation Assignment

This project automates the scraping and analysis of opinion articles from the Spanish news site [El País](https://elpais.com), including cross-browser testing using BrowserStack.

## Features

- Navigate to the **Opinión** section of El País.
- Extract the **title**, **content**, and **cover image** of the first 5 articles.
- Translate titles to English using the **Google Translate API**.
- Identify and print **repeated words** across translated titles.
- Run the full test flow locally and in parallel across 5 environments on **BrowserStack**.

## Project Structure
browserstack_assignment/
├── scraper.py # Core scraping logic
├── translator.py # Google Translate API integration
├── analyzer.py # Repeated words analysis
├── images/ # Downloaded article images
├── tests/
│ ├── test_scraper.py # Local run
│ └── test_browserstack.py # Parallel cross-browser run
├── requirements.txt

## Notes
Some mobile configurations may require updated OS versions.
Images are stored in the images/ folder.
Stale element issues are handled with best-effort retries.