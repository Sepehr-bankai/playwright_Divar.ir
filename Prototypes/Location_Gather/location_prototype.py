import asyncio
import csv
from playwright.async_api import async_playwright

# Entry point of the script: launches a Playwright browser to scrape neighborhood names from Divar.ir
async def main():
    data = []

    # Initialize Playwright and launch Chromium browser (headless mode is off for debugging)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # Navigate to the Tehran apartment listings page
        await page.goto("https://divar.ir/s/tehran/buy-apartment")

        # Open the sidebar and access the neighborhood filter
        await page.locator('#app > div.browse-c7458.browse--has-map-b4ff7 > div > aside > form > div:nth-child(1)').click()
        await page.locator('#districts > div.raw-button-cd669.kt-action-field.kt-action-field--small > span').click()
        await page.wait_for_selector("#multi-select-modal-list-box > div")

        # Scroll through the modal list to reveal more neighborhoods
        for i in range(30):
            data_locate = page.locator("#multi-select-modal-list-box > div > div > div")
            
            # Scroll down inside the modal
            await page.evaluate("""
                document.querySelector('#multi-select-modal-list-box > div')?.scrollBy(0, 2000);
            """)
            await asyncio.sleep(2)

            # Extract and store visible neighborhood names
            count = await data_locate.count()
            for _ in range(count):
                try:    
                    entry = await data_locate.nth(_).inner_text()
                    data.append(entry.strip())
                    print("Neighborhood name saved.\n")
                except Exception as e:
                    print(f"Error occurred: {e}")

        await browser.close()

    # Save all collected neighborhood names to a CSV file
    with open("divar.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["THE INFORMATION GATHERED IS:"])
        for info in data:
            writer.writerow([info])

# Run the asynchronous scraping function
asyncio.run(main())
