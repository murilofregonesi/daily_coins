from scraper.scraper import Scraper


if __name__ == '__main__':
    scraper = Scraper()

    scraper.get_daily_coins()
    scraper.join_daily_draw()
