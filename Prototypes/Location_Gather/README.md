# 🏙️ Divar Neighborhood Scraper

This is a simple and powerful Python script built with [Playwright](https://playwright.dev/python/) to scrape neighborhood names from Tehran apartment listings on [Divar.ir](https://divar.ir).

## 🚀 What It Does

- Opens the Tehran apartment listings page on Divar.
- Clicks on the sidebar to open the neighborhood filter.
- Scrolls through all available neighborhoods (up to 30 scrolls).
- Extracts the names of neighborhoods.
- Saves the results into a CSV file (`divar.csv`) with UTF-8 encoding.

## 📦 Requirements

Make sure you have Python 3.7+ installed. Then install dependencies:

```bash
pip install -r requirements.txt
playwright install

*****

The browser will open (headless mode is OFF by default so you can debug visually). After it finishes, you’ll find a file named divar.csv in your directory with the scraped neighborhood data.

🛠️ Customization
You can change the number of scrolls from 30 to any other number in the loop.

Set headless=True in p.chromium.launch() to avoid opening the browser window.

⚠️ Disclaimer
This project is for educational purposes only. Please respect Divar.ir's terms of service and avoid aggressive scraping.
