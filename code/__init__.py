#from zenrows import ZenRowsClient
import cloudscraper
from zenrows import ZenRowsClient
import env
from code.scraper.house import get_house_data
from database import Database


# HOUSING MEXICO!
class HousingMexico:
    
    # initialize HousingMexico
    def __init__(self, debug = True, useDB = False, longDescriptions = False, use_zenrows = True):

        # this creates the scraper
        self.use_zenrows = use_zenrows

        if self.use_zenrows:
            self.scraper = ZenRowsClient(env.ZENROWS_KEY)
        else:
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
        get_house_data(self.scraper, self.debug, self.db, self.longDescriptions, self.use_zenrows)
