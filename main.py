from code import HousingMexico
from database import load_database

# initialize HousingMexico
scraper = HousingMexico()

# initialize database
db = load_database()

# obtain housing data
data = scraper.get_data()