#from zenrows import ZenRowsClient
import cloudscraper

from code.scraper.house import get_house_data
from database import Database


# HOUSING MEXICO!
class HousingMexico:
    
    # initialize HousingMexico
    def __init__(self, debug = True, useDB = False, longDescriptions = False):

        # this creates the scraper
        #self.scraper = ZenRowsClient("84e2f89ab2e28c2b21846cb7f7644bab6f40db15")
        self.scraper = cloudscraper.create_scraper()
        print("Scraper has been initialized")

        # set debug mode
        self.debug = debug

        # set long descriptions
        self.longDescriptions = longDescriptions

        # set if db is to be used
        self.db = Database() if useDB == True else None


    # obtain house data
    def get_data(self):

        # self.db is database is accepted else None
        get_house_data(self.scraper, self.debug, self.db, self.longDescriptions)
