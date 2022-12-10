import cloudscraper
from code.scraper.house import get_house_data


# HOUSING MEXICO!
class HousingMexico:
    
    # initialize scraper
    def __init__(self):
        self.scraper = cloudscraper.create_scraper()

    # obtain house data
    def get_data(self):
        get_house_data(self.scraper)