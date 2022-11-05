import asyncio

from playwright.async_api import async_playwright


class Scraper:
    def __init__(self) -> None:
        pass

    async def test_scraper(self) -> None:
        # async with async_playwright() as pw:
        #     browser = await pw.chromium.launch(headless=False)
        #     page = await browser.new_page()
        #     await page.goto('https://shopee.com.br/shopee-coins')

        #     await asyncio.sleep(5)
        #     print(await page.title())
        #     await page.screenshot(path="data/example.png")

        #     await browser.close()

        user_data_dir = "/tmp/test-user-data-dir"

        async with async_playwright() as pw:
            # Prepare browser
            browser = await pw.firefox.launch_persistent_context(user_data_dir, headless=False)
            page = await browser.new_page()

            await page.goto('https://shopee.com.br/buyer/login?next=https%3A%2F%2Fshopee.com.br%2Fshopee-coins')

            # Login
            try:
                await page.get_by_text('Google').click()

                async with page.expect_event('popup') as page_info:
                    popup = await page_info.value

                    field = popup.get_by_role('textbox')
                    await field.type('')
                    await field.press("Enter")

                    await asyncio.sleep(2)
                    
                    field = popup.get_by_role('textbox')
                    await field.type('')
                    await field.press("Enter")
                    
                    await asyncio.sleep(5)
            except:
                print('No MFA required.')
            
            # Get coin
            try:
                await page.get_by_text('Clique para ganhar 1 moeda').click()
                print('Ganhar moeda.')
                await page.screenshot(path="data/coin.png")
            except:
                print('Moeda já resgatada.')
            
            # Draw
            try:
                await page.get_by_text('Resgate até 1000 Moedas!').click()
                print('Acessando página do sorteio.')
                await asyncio.sleep(5)
                await page.screenshot(path="data/draw.png")

                await page.query_selector('#clickArea').click()  # id="clickArea"
                print('Sorteio realizado.')
            except:
                print('Sorteio já realizado.')
            
            await asyncio.sleep(1520)
            await browser.close()
