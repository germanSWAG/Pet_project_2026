import asyncio 
from playwright.async_api import async_playwright, Page
from urllib.parse import urlparse
import re
import httpx 




class DromSource:

    def __init__(self, page : Page):
        self.page = page


    async def get_count_car(self, url : str):
        await self.page.goto(url)
        await self.page.wait_for_selector('[data-ftid="bulls-list_bulls-tab"]')
        count = self.page.locator('[data-ftid="bulls-list_bulls-tab"]')

        count_el = await count.inner_text()
        return count_el


    async def get_links_brands(self, city : str):
        await self.page.goto(f"https://auto.drom.ru/{city}/")

        links = self.page.locator(
            '[data-ftid="component_cars-list-item_hidden-link"]'
            )
            
        count = await links.count()

        brands = []

        for i in range(count):
            link = links.nth(i)

            name = (await link.inner_text()).strip()
            url = await link.get_attribute("href")

            if not url:
                continue

            brands.append({"name" : name, "url" : url})
        
        return brands
    
    async def get_cars(self, url : str):
        
        city, brand = urlparse(url).path.strip('/').split('/')
        
        
        print(url)

        page = 99

        seen = set()

        while page <= 100:
            url_page = f"{url.rstrip('/')}/page{page}"
            print(url_page)

               

            await self.page.goto(url_page)

            await self.page.wait_for_selector('[data-ftid="bulls-list_bull"]')

            cards = self.page.locator('[data-ftid="bulls-list_bull"]')


            count = await cards.count()
            if count == 0:
                print("Ограничение глубины пагинации")
                break
            page_data = []


            for i in range(count):
                card = cards.nth(i)
                   

                sold_badge = card.locator('[data-ftid="bull_sold"]')
                title_el = card.locator('[data-ftid="bull_title"]')
                # sub_el = card.locator('[data-ftid="bull_subtitle"]')
                price_el = card.locator('[data-ftid="bull_price"]')

                if await sold_badge.count() > 0:
                    print("Автомобиль был продан. Объявление проигнорированно")
                    continue


                if await title_el.count() > 0:
                    title = await title_el.inner_text()
                    price = await price_el.inner_text()
                    # equipment = await sub_el.inner_text()

                    clean_price = ''.join(re.findall(r'\d+', price))

                    href = await title_el.get_attribute("href")

                    if href in seen:
                        continue
                    seen.add(href)
                        

                        
                    page_data.append({
                            "brand" : brand,
                            "title" : title,
                            "price" : clean_price,
                            "city" : city,
                            "href" : href
                            })
            if page_data:
                yield page_data

                page += 1
                
            



            
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        

        drom = DromSource(page)
        brands = await drom.get_links_brands('moscow')

        async with httpx.AsyncClient() as client:
            for brand in brands:
                url = brand['url']
                async for cars_batch in drom.get_cars(url):
                    response = await client.post(
                    "http://localhost:8000/items",
                    json=cars_batch)
                    print(response.status_code)
                    print(f"Отправлено {len(cars_batch)} Объявлений")

                

        count = await drom.get_count_car(url)

        
        print(brands)
        city = {'region23' : 'krasnodar'}

        # async for cars_batch in drom.get_cars():
        #     print(f'Получены новые данные машин из {len(cars_batch)}')

        #     for car in cars_batch:
        #         print(f'Обработка: {car['title']} за {car['price']} руб.  Ссылка - {car['href']}')




        await browser.close()

        
            




if __name__ == "__main__":
    asyncio.run(main())
        

