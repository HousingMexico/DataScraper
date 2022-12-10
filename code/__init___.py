import cloudscraper
from scraper.house import get_house_data

# HOUSING MEXICO!
class HousingMexico:
    
    # initialize scraper
    def __init__(self):
        self.scraper = cloudscraper.create_scraper()

    # obtain information
    def get_data(self):
        get_house_data(self.scraper)