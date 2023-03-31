from bs4 import BeautifulSoup
import re

# URL to fetch information
URL = 'https://www.inmuebles24.com/'

# obtain house information
def get_house_data(scraper, debug, db):

    # inmuebles24 shows estate on page index
    for page in range(1, 5):

        # obtain website where houses are listed (20 houses per page)
        driver = scraper.get(URL + 'casas-en-venta-en-ciudad-de-mexico' + '-pagina-' + str(page) + '.html').text
        # parse main HTML
        soup = BeautifulSoup(driver, 'html.parser')

        # locate properties (individual divs)
        individualDivs = soup.find_all('div', {"class": "sc-i1odl-0 kJzCBs"})
        # it will extract the link to the individual page of each property

        # loop through each div and obtain each individual house inforation
        for idividualHouse in individualDivs:

            # base URL where the route of the div will be added

            # data-to-posting is the attribute that contains the link of individual homes
            # link of each individual house 
            houseLink = URL + str(idividualHouse['data-to-posting'])
            print(f"LINK: {houseLink}") if debug == True else None


            # get the individual house website content
            houseWebsite = scraper.get(houseLink).text

            # parse individual house website
            soupInd = BeautifulSoup(houseWebsite, 'html.parser')

            # this is now triggered inside the individual house website
            # obtain the page title which has the name of the house
            houseNameH1 = soupInd.find("h1").text
            print(f"HOUSENAME: {houseNameH1}") if debug == True else None
            

            # Obtain price (span) inside the div of the price item
            housePrice = soupInd.find("div", {"class":"price-items"}).find("span")

            # remove non-numbers (mainly MXN and numer commas)
            housePrice = re.sub('[^0-9]', '', housePrice.text.strip())
            print(f"HOUSEPRICE: {housePrice}") if debug == True else None 

            # It will find the hgroup attribute and extract the span where the location is located
            location = soupInd.find("hgroup", {"class":"title-container"}).find("span").text
            
            # Separate the zone from the city hall and remove whitespaces
            zone = location.split(',')[1].lstrip()
            city_hall = location.split(',')[2].lstrip()
            print(f"Zone: {zone}") if debug == True else None
            print(f"City hall: {city_hall}") if debug == True else None

            # obtain house information: size, bedrooms, etc
            houseChar = soupInd.find("ul", {"class":"section-icon-features"}).find_all("li") 
            houseCharacteristics = {
                "size": "", 
                "built": "", 
                "fullbathrooms": "", 
                "parking": "", 
                "bedrooms": "", 
                "halfbathrooms": "", 
                "years": "", 
            }

            # loop through items
            for item in houseChar:
                
                # clean the string (full of whitespaces, a mess)
                # remove every non-alphanumerican value
                new = re.sub('[^0-9A-Za-zÑñ]', '', item.text)

                # TODO: REFACTOR THIS CODE!!
                
                # list every possible house characteristic
                characteristics = ["total", "construido", "baño", "estacionamiento", "recmara", "medio", "antigedad", "aestrenar"]
                actualCharacteristics = ["size", "built", "fullbathrooms", "parking", "bedrooms", "halfbathrooms", "years", "years"]
                
                # loop through the characteristics
                # get index for the actual characteristics' position
                for i, char in enumerate(characteristics):

                    # if a characteristic is found in the body, then:
                    # 1. remove every NaN digit
                    # 2. store it in the characteristics dictionary
                    if char in new.lower():
                        final = re.sub('[^0-9]', '', new)
                        houseCharacteristics[actualCharacteristics[i]] = final
                        # this final line sets a real item into the dictionary and not a miss-spelled word

            print(houseCharacteristics) if debug == True else None

            # register the house in the database if parameter is True in root's main.py
            houseData = {
                "link": houseLink,
                "name": houseNameH1,
                "price": housePrice,
                "zone": zone,
                "city_hall": city_hall,
                "details": houseCharacteristics
            }            
            db.storeHouseInformation(houseData) if db != None else None
