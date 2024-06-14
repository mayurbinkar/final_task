import asyncio   # asyncio library is used to syncronise url await is syntax 
from playwright.async_api import async_playwright 
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

async def scrape_flipkart_mobiles():
    # Usage Playwright
    async with async_playwright() as p:
        # running browser
        browser = await p.chromium.launch(headless=True)
        # opening browser
        page = await browser.new_page()
        
        # implementing proxy and headers
        await page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })

        # Going to the Flipkart search results page
        await page.goto("https://www.flipkart.com/search?q=mobiles&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off")

        mobileData = []

        # Scrape multiple pages by applying range 
        for i in range(50):
            # Wait for the necessary content to scrap
            await page.wait_for_selector('div.tUxRFH')
            #await page.wait_for_timeout(2000) 
            
            # Extraction from the current page
            dContent = await page.content()
            #print(dcontent)   
            soup = BeautifulSoup(dContent, 'html.parser')
            for item in soup.find_all('div', class_='tUxRFH'): #container class of all data
                titleTag = item.find('div', class_='KzDlHZ')
                descriptionTag = item.find('ul', class_='G4BRas')  #ul tag conatins all li tags that have data on it 
                priceTag = item.find('div', class_='Nx9bqj _4b5DiR')  #selling price
                maximumPriceTag = item.find('div', class_='yRaY8j ZYYwLA')  #Mrp price which is return at bottom near to price
                ratingTag = item.find('div', class_='XQDdHH')
                productUrlTag = item.find('a')['href']
                if titleTag and priceTag:

                    title = titleTag.text if titleTag else 'N/A'

                    description = descriptionTag.text if descriptionTag else 'N/A'

                    priceValue = priceTag.text if priceTag else 'N/A'
                    # Getting integer value using regular expression
                    price = re.sub(r'\D', '', priceValue)

                    brand = title.split()[0]  # Assuming brand is the first word in the title so we give 0 th index value 

                    MaxPrice = maximumPriceTag.text if maximumPriceTag else 'N/A'

                    mrp = re.sub(r'\D', '', MaxPrice)

                    rating = ratingTag.text if ratingTag else 'N/A'

                    product_url = 'https://www.flipkart.com' + productUrlTag    # by using this we can write  https://www.flipkart.com at the start of urls

                    mobileData.append({ 'Brand': brand,
                                        'Title': title,
                                        'Description': description,
                                        'Price': price,
                                        'MRP': mrp,
                                        'Rating': rating,
                                        'Url': product_url})   #collecting data frame by key values

            # Click on the "Next" button to go to the next page
            next_button = await page.query_selector('a._9QVEpD:has-text("Next")')
            if next_button:
                await next_button.click()
                #await page.wait_for_load_state('networkidle')  # Wait for the next page to load
                #time.sleep(5)  # Additional sleep to ensure the page is fully loaded
            else:
                break  # Exit from loop aftere reaching its limits

        # Clossing the browser
        await browser.close()

        # Using Pandas create dataframe
        df = pd.DataFrame(mobileData)

        # Save the df to a CSV file
        df.to_csv('flipkart_mobiles_data50_Pages.csv', index=False)

        # Print the DataFrame to get data
        print(df)

# Run the scrape_flipkart function
asyncio.run(scrape_flipkart_mobiles())
