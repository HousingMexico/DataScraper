import cloudscraper
from code.scraper.house import get_house_data
from database import Database


# HOUSING MEXICO!
class HousingMexico:
    
    # initialize HousingMexico
    def __init__(self, useDB = False):

        # this creates the scraper
        self.scraper = cloudscraper.create_scraper(browser = {
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        })

        # set if db is to be used
        self.db = Database() if useDB == True else None


    # obtain house data
    def get_data(self):

        # self.db is database is accepted else None
        get_house_data(self.scraper, self.db)
