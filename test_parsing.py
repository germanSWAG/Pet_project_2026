import asyncio 
from playwright.async_api import async_playwright
from fake_useragent import FakeUserAgent

async def parser(brand : str, region = str| None):
    if region:
        url = f'https://auto.drom.ru/{region}/{brand}/all/'
    url = f'https://auto.drom.ru/{brand}/'
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
        for car in card[:19]:
            models = car.locator('[data-ftid="bull_title"]')
            price = car.locator('[data-ftid="bull_price"]')
            models_text = await models.inner_text()
            price_text = await price.inner_text()
            link = await models.get_attribute('href')
            parsed.append({"model" : models_text.split(', '),
             "price" : price_text.strip().replace('\xa0', ''), 
             "link" : link})
        print(parsed)
        print("Успешно")
        print(len(parsed))

        # for car in parsed:
        #     if int(car['price']) <= 200000 and int(car['model'][1]) >=2001:
            
        #         print(car)
        await browser.close()


asyncio.run(parser("mercedes-benz"))
        
