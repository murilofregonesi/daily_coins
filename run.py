import asyncio

from scraper.scraper import Scraper


if __name__ == '__main__':
    asyncio.run(Scraper().test_scraper())
