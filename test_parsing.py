import asyncio 
from playwright.async_api import async_playwright
from fake_useragent import FakeUserAgent
import re
import json

async def parser(brand : str, region : str| None = None):
    if not region:  
        url = f'https://auto.drom.ru/{brand}/'
    else:
        url = f'https://auto.drom.ru/{region}/{brand}/all/'
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, 
        args=["--disable-blink-features=AutomationControlled"])
        user_agent = FakeUserAgent().random
        context = await browser.new_context(user_agent=user_agent, viewport={'width': 1280, 'height': 720})
        page = await context.new_page()
        await page.goto(url=url, wait_until='domcontentloaded')
        await page.wait_for_selector('[data-ftid="bulls-list_bull"]', timeout=10000)
        card = await page.locator('[data-ftid="bulls-list_bull"]').all()
        
        print(f"Найдено карт {len(card)}")

        parsed = []
        for car in card:
            models = car.locator('[data-ftid="bull_title"]')
            price = car.locator('[data-ftid="bull_price"]')
            models_text = await models.inner_text()
            price_text = await price.inner_text()
            link = await models.get_attribute('href')
            parts = tuple(filter(None, re.split(r",|\s+", models_text)))

            brand = parts[0]
            year = parts[-1]
            model = " ".join(parts[1:-1])
            parsed.append({
            "brand" : brand,
            "model" : model,
            "year" : year,
            "price" : price_text.strip().replace('\xa0', ''), 
            "link" : link
            })

        with open('data/info_cars.json', 'w', encoding='utf-8') as f:
            data = json.dump(parsed, f, indent=2)
            

        print(len(parsed))

        for i in parsed:
            if i['model'] == 'C-Class':
                print(i)

        # for car in parsed:
        #     if int(car['price']) <= 200000 and int(car['model'][1]) >=2001:
            
        #         print(car)
        await browser.close()



if __name__ == "__main__":
    asyncio.run(parser("mercedes-benz", region="krasnodar"))
        

