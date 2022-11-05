import os
from typing import Any

from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

from scraper.utils.constants import TIMEOUT, USER_DATA_DIR


load_dotenv()


class Scraper:
    def __init__(self) -> None:
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.firefox\
            .launch_persistent_context(USER_DATA_DIR, headless=False)

    def __del__(self) -> None:
        if self.playwright and self.browser:
            self.browser.close()
            self.playwright.stop()

    def new_page_logged_in(self) -> Any:
        """Performs login and returns a new page.
        With persistent context, MFA should be required just once.
        """
        print('* Realizar login.')
        page = self.browser.new_page()
        page.set_default_timeout(TIMEOUT)

        page.goto('https://shopee.com.br/buyer/login?next=https%3A%2F%2Fshopee.com.br%2Fshopee-coins')
        page.wait_for_load_state()

        try:
            page.get_by_text('Google').click()

            with page.expect_event('popup') as page_info:
                popup = page_info.value

                field = popup.get_by_role('textbox')
                field.type(os.getenv('USER_EMAIL'))
                field.press("Enter")

                page.wait_for_load_state()

                field = popup.get_by_role('textbox')
                field.type(os.getenv('USER_PASSWORD'))
                field.press("Enter")

                page.wait_for_load_state()
        except Exception as error:
            print('No MFA required.')
            print(error)

        print('Login realizado.')
        return page

    def get_daily_coins(self) -> None:
        """Get daily coins. Previous login is required."""
        print('* Ganhar moeda diária.')
        page = self.new_page_logged_in()

        try:
            page.get_by_text('Clique para ganhar 1 moeda').click()
            page.screenshot(path="data/coin.png")
        except Exception as error:
            print('Moeda já resgatada.')
            print(error)

        page.close()

    def join_daily_draw(self) -> None:
        """Get daily coins. Previous login is required."""
        print('* Sorteio diário.')
        page = self.new_page_logged_in()

        try:
            print('Acessando página do sorteio.')
            page.get_by_text('Resgate até 1000 Moedas!').click()
            page.wait_for_load_state()
            page.screenshot(path="data/draw.png")
        except Exception as error:
            print('Sem acesso à página do sorteio.')
            print(error)
            return

        try:
            page.frame_locator("#main iframe").locator("#clickArea").click()
            print('Sorteio realizado.')
        except Exception as error:
            print('Sorteio já realizado.')
            print(error)

        page.close()
