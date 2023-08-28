from bs4 import BeautifulSoup
import re

# URL to fetch information
URL = 'https://www.inmuebles24.com/'

# obtain house information
def get_house_data(scraper, debug, db):

    # inmuebles24 shows estate on page index
    for page in range(1, 4):

        # obtain website where houses are listed (20 houses per page)
        driver = scraper.get(URL + 'casas-en-venta-en-ciudad-de-mexico' + '-pagina-' + str(page) + '.html').text
        # parse main HTML
        soup = BeautifulSoup(driver, 'html.parser')

        # obtain specific house links
        links = soup.find_all('a', {"class": "sc-i1odl-11 kptTyQ"})

        # loop through each div and obtain each individual house inforation
        for link in links:

            # base URL where the route of the div will be added
            baseURL = 'https://www.inmuebles24.com'

            # data-to-posting is the attribute that contains the link of individual homes
            # link of each individual house 
            houseLink = baseURL + link.get("href")
            print(f"LINK: {houseLink}") if debug == True else None

            # parse individual house website
            house = scraper.get(houseLink).text
            # parse main HTML
            soupInd = BeautifulSoup(house, 'html.parser')

            # this is now triggered inside the individual house website
            # obtain the page title which has the name of the house
            houseNameH1 = soupInd.find("h1").text
            print(f"HOUSENAME: {houseNameH1.strip()}") if debug == True else None
            
            # obtain price (span) inside the div of the price item
            housePrice = soupInd.find("div", {"class":"price-items"}).find("span")

            # remove non-numbers (mainly MXN and numer commas)
            housePrice = re.sub('[^0-9]', '', housePrice.text.strip())
            print(f"HOUSEPRICE: {housePrice}") if debug == True else None 

            # It will find the hgroup attribute and extract the span where the location is located
            locationDirty = soupInd.find("h2", {"class":"title-location"}).find("span")
            location = str(locationDirty).replace("<span>", "").replace("</span>", "")

            # Separate the zone from the city hall and remove whitespaces
            zone = location.split(',')[1].lstrip()
            city_hall = location.split(',')[2].lstrip()
            print(f"Zone (Colonia): {zone}") if debug == True else None
            print(f"City hall (Alcaldía): {city_hall}") if debug == True else None

            # obtain house information: size, bedrooms, etc
            houseChar = soupInd.find_all("li", {"class": "icon-feature"})
            houseCharacteristics = {
                "size": "", 
                "built": "", 
                "fullbathrooms": "", 
                "parking": "", 
                "bedrooms": "", 
                "halfbathrooms": "", 
                "years": "", 
            }

            # set a local variable to see if house is complex or not (will use later)
            isComplex = [False]

            # loop through items
            for item in houseChar:

                # clean the string (full of whitespaces, a mess)
                # remove every non-alphanumerican value
                new = re.sub('[^0-9A-Za-zÑñ]', '', item.text)
                
                # VERIFY IF HOUSE IS A COMPLEX OR SINGLE HOUSE
                # run in try-except because if UL is not found it will raise an exception
                try:
                    # check if house is individual or complex (we do not want complexes)
                    # basically: complexes have an 'ul' tah saying with the string "un."
                    # if that string is found, break the execution
                    index = str(new.lower()).index("uni")
                    print("House is NOT an individual home") if debug == True else None
                    # this is necessary to acces nonlocal (scope) variables
                    isComplex[0] = True
                    break # destroys flagged house iteration
                except:
                    pass # ignore exception

                # TODO: REFACTOR THIS CODE!!
                
                # list every possible house characteristic
                characteristics = ["total", "construido", "baños", "estacionamiento", "recmara", "mediobaño", "antigedad", "aestrenar"]
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

            if isComplex[0] == True:
                print("Destroyed house iteration") if debug == True else None
                continue # skip to next house (avoid database insertion)
            
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