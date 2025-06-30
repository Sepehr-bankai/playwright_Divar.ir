import asyncio
import csv 
from playwright.async_api import async_playwright
from .image_blocker import image_blocker
from .gather_links import gather_links
from .neighborhood_finder import combination
from .numeric_func import number_changer

#A function to gather info based on links i have gathered via using Gather_link() function.
async def gather_info(all_links):

    #An Empty dictionary ready for my Final data when the are ordered and seperated.
    final_data = []



    async with async_playwright() as p:
       
        #a counter to count my For Loop and tell each time when its trying to gather info.
        counter = 0

        #Setting up my Browser, i prefer it headless.
        browser = await p.chromium.launch()
        page = await browser.new_page()

        #Blocking Images to decrease data usage and speeding up the process.
        await page.route("**/*", image_blocker)


        #loop to help us doing our Process on each Links provided to us via Last Function.
        for i in all_links:

            
            counter += 1

            #to avoid Crashing out and better understanding this process is functioning well.
            try:

                #My connection is poor so i set a timeout on 40Seconds and,
                #Im seaching each Link Via For Loop.
                await page.goto(i, timeout=40000)
                
                #By this message i would be notified which Link out of how many Links is getting done.
                print(f"Trying {counter}/{len(all_links)} -> {i}")


                await page.wait_for_selector("#app > div.container--has-footer-d86a9.kt-container")

                #Locating our District, 
                #it could be done in Last function(in post list),
                #but it would have turned messy! i prefer it clean and easier.
                neighborhood = await page.locator(
                    '#app > div.container--has-footer-d86a9.kt-container > div > main > article > div > div.kt-col-5 > section:nth-child(1) > div.kt-page-title > div > div'
                ).inner_text()


                #This part get a list with (\n) seperating the,
                #informations, which are the space in meter,
                #the Year that structure was built and Rooms in total.
                numeric_details = await page.locator(
                    "#app > div.container--has-footer-d86a9.kt-container > div > main > article > div > div.kt-col-5 > section:nth-child(1) > div.post-page__section--padded > table:nth-child(1) > tbody > tr"
                ).all_inner_texts()

                #Changing Arabic numbers into English so we could easily use PANDAS and ETC...
                eng_numeric_details = [number_changer(item) for item in numeric_details]


                #This locator get inner text of price for each meter.
                price_per_meter = await page.locator(
                    '#app > div.container--has-footer-d86a9.kt-container > div > main > article > div > div.kt-col-5 > section:nth-child(1) > div.post-page__section--padded > div:nth-child(7) > div.kt-base-row__end.kt-unexpandable-row__value-box > p'
                ).inner_text()
                eng_price_per_meter = number_changer(price_per_meter)


                #to first part my string into 3 unrelated parts.
                raw_details = eng_numeric_details[0]
                parting = [x.strip() for x in raw_details.split("\n") if x.split()]
                numeric_info = {
                    "meter":parting[0],
                    "year":parting[1],
                    "rooms":parting[2]
                }


                #A function to seperate our District name from the string we do not need.
                #Which had the time of posting this ad.
                neighborhood_final = combination(neighborhood)
                

                #Finally using our empty dictionary and appending all above details,
                #before ending the loop which earaise our current info we gathered.
                final_data.append({
                    "price per meter": eng_price_per_meter,
                    "meter": numeric_info["meter"],
                    "year": numeric_info["year"],
                    "rooms": numeric_info["rooms"],
                    "neighborhood": neighborhood_final
                })


            #So we Would know What caused our Error and we can fix it sooner.
            except Exception as e:
                print(f"Error {e} occurred on link: {i}\n")



        await browser.close()


    #Creating a csv file and pouring all data we gathered based on Links amount,
    #and after this we have So much real Data and we can use it on our other Projects.
    with open("Final_info.csv", mode="w", newline='', encoding="utf-8") as file:
        fieldnames = ["price per meter", "meter", "year", "rooms", "neighborhood"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for item in final_data:
            writer.writerow(item)

    #Done
    print("Files are saved Succesfuly.\n")
