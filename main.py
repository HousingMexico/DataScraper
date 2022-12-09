from code import HousingMexico

# initialize HousingMexico
scraper = HousingMexico()

# obtain housing data
data = scraper.get_data()

# debug!
print(data)
