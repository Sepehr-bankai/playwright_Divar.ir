import asyncio
from playwright.async_api import async_playwright
from .image_blocker import image_blocker


#just in case the user doesnt add any links or scroller amount,
#i have to mention this code works for now but you need to,
#add LOCATOR.CLICK() because page ends on 20/21 scrolles.
async def gather_links(scroll=13, url="https://divar.ir/s/tehran/buy-apartment?bbox=51.3111305%2C35.755619%2C51.3498192%2C35.770977&map_bbox=51.310424%2C35.753166%2C51.349115%2C35.768525&map_place_hash=1%7C%7Capartment-sell"):
    
    #We Need A set in case we dont confront any Duplicates,
    #this could be done in next function but this method was easier and cleaner.
    seen = set()
    all_links = []

    print("program running...")

    async with async_playwright() as p:

        #i prefer it headless, you can change it easily.
        browser = await p.chromium.launch()
        page = await browser.new_page()

        #Blocking Images to decrease data usage and speeding up the process.
        await page.route("**/*", image_blocker)

        #My connection is poor so i set a timeout on 40Seconds and,
        await page.goto(url, timeout=40000)

        
        #I added gathering at fist 
        for scroll_index in range(scroll):
            try:

                #just in case so that if we confronted anyy Error,
                #we can easilly find and fix it.
                await page.wait_for_selector("#post-list-container-id")
            
            #i always prefer f string so it looks better:).
            except Exception as e:
                print(f"Error waiting for main container: {e}")

            links = page.locator("#post-list-container-id div.post-list-eb562 div > div > div > article > a")
            count = await links.count()

            #i always prefer the program talks a bit so i can feel its alive(weird i know)
            print(f"{count} links found.\n")

            #a loop to get the links of the post, then adding the web address,
            #in first i had problem then i found out it could be done easily via f string,
            #and i could check whether it was used or not.
            for link_index in range(count):
                try:
                    href = await links.nth(link_index).get_attribute("href")
                    if not href:
                        continue
                    full_url = f"https://divar.ir{href}"
                    if full_url not in seen:
                        all_links.append(full_url)
                        seen.add(full_url)
                        print(f"Added: {full_url}")
                except Exception as e:
                    print(f"Error {e}, Occured.\n")
            

            #i have to add that this web page which apartments are posted,
            #doesnt scroll via wondow scroller so i found it and this could be done,
            #via JS.
            await page.evaluate("""
                document.querySelector('#app > div.browse-c7458.browse--has-map-b4ff7 > main > div > div.content-dd848')
                ?.scrollBy(0, 2000);
            """)

            #its good to know where the process is heading and where it is now.
            print(f"Scrolling for {scroll_index + 1} time...")

        await browser.close()

    #we would return all the founded links into the variable,
    #which is used on calling us and gonna be used to process the program.    
    return all_links
