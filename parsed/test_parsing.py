import asyncio 
from playwright.async_api import async_playwright, Page
import re




class DromSource:

    def __init__(self, page : Page):
        self.page = page

    async def get_brands(self,):
        await self.page.goto("https://auto.drom.ru/")

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
    
    async def get_cars(self, links : list[dict]):
        
        url = links

        # for link in links[:1]:
            # url = link["url"]
            # model = link["name"]

        while True:
            for num_page in range(1,1000):
                url_page = f'{url + 'page' + str(num_page)}'
                print(url_page)

                try:

                    await self.page.goto(url_page)

                    await self.page.wait_for_selector('[data-ftid="bulls-list_bull"]')
                    await asyncio.sleep(3)

                    cards = self.page.locator('[data-ftid="bulls-list_bull"]')
                except Exception as e:
                    print(f"Страницы закончились {e} или ошибка ошибка на {num_page}")
                    break


                count = await cards.count()
                print(count)
                page_data = []


                for i in range(count):
                    card = cards.nth(i)
                   


                    title_el = card.locator('[data-ftid="bull_title"]')
                    # sub_el = card.locator('[data-ftid="bull_subtitle"]')
                    price_el = card.locator('[data-ftid="bull_price"]')


                    if await title_el.count() > 0 and await price_el.count() > 0:
                        title = await title_el.inner_text()
                        price = await price_el.inner_text()
                        # equipment = await sub_el.inner_text()

                        clean_price = ''.join(re.findall(r'\d+', price))

                        href = await title_el.get_attribute("href")
                        

                        
                        page_data.append({
                                # "brand" : model,
                                "title" : title,
                                "price" : clean_price,
                                "href" : href
                            })
                if page_data:
                    yield page_data

                await asyncio.sleep(5)
            break



            
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        drom = DromSource(page)
        brands = await drom.get_brands()

        brand = 'https://auto.drom.ru/krasnodar/audi/'

        async for cars_batch in drom.get_cars(brand):
            print(f'Получены новые данные машин из {len(cars_batch)}')

            for car in cars_batch:
                print(f'Обработка: {car['title']} за {car['price']} руб.  Ссылка - {car['href']}')




        await browser.close()

        
            




if __name__ == "__main__":
    asyncio.run(main())
        

