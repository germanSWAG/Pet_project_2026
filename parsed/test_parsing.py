import asyncio 
from playwright.async_api import async_playwright, Page





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

        data = []

        for link in links[2:]:
            url = link["url"]
            model = link["name"]

            await self.page.goto(url)

            await self.page.wait_for_selector('[data-ftid="bulls-list_bull"]')

            cards = self.page.locator('[data-ftid="bulls-list_bull"]')

            count = await cards.count()

            for i in range(count):
                card = cards.nth(i)


                title_el = card.locator('[data-ftid="bull_title"]')
                sub_el = card.locator('[data-ftid="bull_subtitle"]')
                price_el = card.locator('[data-ftid="bull_price"]')

                title = await title_el.inner_text()
                price = await price_el.inner_text()
                equipment = await sub_el.inner_text()

                href = await title_el.get_attribute("href")
                

                
                data.append({
                        "brand" : model,
                        "title" : title,
                        "equipment" : equipment,
                        "price" : price,
                        "href" : href
                    })

        return data


            
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        drom = DromSource(page)
        brands = await drom.get_brands()

        cars = await drom.get_cars(brands)

        print(brands)

        await browser.close()

        
            




if __name__ == "__main__":
    asyncio.run(main())
        

