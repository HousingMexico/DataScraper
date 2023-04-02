from code import HousingMexico


# batch of website pages to run
# batch = 0 means websites from 0-9
#batch = 1 would run websites from 10-19
# batch = 2 would run websites from 20-29
batch = 0

# initialize HousingMexico
# param 1: batch to run (clustering: select range of pages to run)
# param 2: debug mode? (True or False)
# param 3: should we use database? (True or False)
scraper = HousingMexico(batch, True, True)

# obtain housing data
data = scraper.get_data()