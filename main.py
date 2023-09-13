from code import HousingMexico

# initialize HousingMexico
# param 1: debug mode? (True or False)
# param 2: should we use database? (True or False)
# param 3: store long house descriptions? (paragraphs explaining house details)
scraper = HousingMexico(True, True, False)

# obtain housing data
data = scraper.get_data()
