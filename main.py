from code import HousingMexico

# initialize HousingMexico
# param 1: debug mode? (True or False)
# param 2: should we use database? (True or False)
scraper = HousingMexico(True, True)

# obtain housing data
data = scraper.get_data()