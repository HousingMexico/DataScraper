import cloudscraper
from code.houseScraper import get_house_data


class HousingScraper:
    def __init__(self):
        self.scraper = cloudscraper.create_scraper()

    def get_data(self):
        get_house_data(self.scraper)
