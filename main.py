from code import HousingMexico

# initialize HousingMexico
# param: should we use database? (True or False)
scraper = HousingMexico(True)

# obtain housing data
data = scraper.get_data()