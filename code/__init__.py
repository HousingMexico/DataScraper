import cloudscraper
from code.scraper.house import get_house_data


class HousingMexico:
    
    def __init__(self):
        self.scraper = cloudscraper.create_scraper()

    def get_data(self):
        get_house_data(self.scraper)