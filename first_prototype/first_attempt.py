import asyncio
from playwright.async_api import async_playwright
import csv


async def main():

    uniq = []

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        #This ling is only for Apartments for sale.
        await page.goto("https://divar.ir/s/tehran/buy-apartment")
        
        #Loop through the currently visible listings on the page.
        #Since only a few items are visible at a time and older ones disappear after scrolling,
        #We extract data in each scroll step to avoid losing previous listing.
        for i in range(21):

            gathered_info = page.locator("#post-list-container-id")

            #I used JS inside evaluate() to scroll the dunamic container og Divar,
            #Since the page doesnt scroll via window.scroll and the post list
            #is inside a scrollable div.
            #You must still replace the Page.evaluate() with await page.evaluate("window.scrollBy(0,1000)"),
            #for other pages that you are able to scroll via window.scroll.
            await page.evaluate(
                """
                document.querySelector('#app > div.browse-c7458.browse--has-map-b4ff7 > main > div > div.content-dd848')?.scrollBy(0, 2000);
            """
            )
            await asyncio.sleep(2)

            #Loop through all currently visible elements matching the selector.
            #Use .count() to get the total number of matches,
            #the extract each items inner text using .nth().
            #Collected texts are stored in a set to automatically remove duplicates.
            count = await gathered_info.count()
            for _ in range(count):
                try:
                    entry = await gathered_info.nth(_).inner_text()
                    uniq.append(entry.strip())
                except Exception as e:
                    print(f"Error {e} occurd.\n")

        print(f"Phase {i} of data gathering, DONE!\n")
        await browser.close()
    with open("divar.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["THE INFORMATION GATHERED IS :"])
        for i in uniq:
            writer.writerow([i])


asyncio.run(main())
