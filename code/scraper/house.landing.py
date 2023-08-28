from bs4 import BeautifulSoup
import re

# URL to fetch information
URL = 'https://www.inmuebles24.com/'

# obtain house information
def get_house_data(scraper, debug, db):

    # inmuebles24 shows estate on page index
    for page in range(1, 2):

        # obtain website where houses are listed (20 houses per page)
        driver = scraper.get(URL + 'casas-en-venta-en-ciudad-de-mexico' + '-pagina-' + str(page) + '.html').text
        
        # parse main HTML
        soup = BeautifulSoup(driver, 'html.parser')

        # obtain specific house divs
        houses = soup.find_all("div", {"class": "sc-i1odl-2 kMrxDq"})

        # loop through each div and obtain each individual house inforation
        for house in houses:
            
            # run in try-except because if UL is not found it will raise an exception
            try:
                # check if house is individual or complex (we do not want complexes)
                # basically: complexes have an 'ul' tah saying with the string "un."
                # if that string is found, break the execution
                houseType = house.find('ul', {'class': 'sc-i1odl-16 eemioV'})
                complex = houseType.find("li")
                index = str(complex).index("un.")
                print("House is NOT an individual home") if debug == True else None
                continue # starts the next iteration
            except:
                pass # ignore exception
            
            # at this point, complex houses have been removed

            # obtain house name
            houseName = house.find("div", {"class": "sc-ge2uzh-0 eXwAuU"}).text
            print(f"HOUSENAME: {houseName.strip()}") if debug == True else None

            # obtain house price
            housePrice = house.find("div", {"class": "sc-12dh9kl-4 hbUMaO"})
            # remove non-numbers (mainly MXN and numer commas)
            housePrice = re.sub('[^0-9]', '', housePrice.text.strip())
            print(f"HOUSEPRICE: {housePrice}") if debug == True else None 

            # obtain house location
            location = house.find("div", {"class":"sc-ge2uzh-2 jneaYd"}).text
            print(location)
            # Separate the zone from the city hall and remove whitespaces
            zone = location.split(',')[0].lstrip()
            city_hall = location.split(',')[1].lstrip()
            print(f"Zone (Colonia): {zone}") if debug == True else None
            print(f"City hall (Alcaldía): {city_hall}") if debug == True else None

            # obtain house information: size, bedrooms, etc
            # 1. obtener el div que tiene todos los spans
            # 2. obtener los spans en una lista
            houseCharDiv = house.find("div", {"class": "sc-1uhtbxc-0 eTeBuc"})
            houseCharSpans = houseCharDiv.find_all("span")

            # ahora: en cada span, hay una imagen con el logo y otro span diferente con el label
            # en el try, filtramos la imagen y enn caso de que sí la haya no hacer nada
            chars = []
            for span in houseCharSpans:
                try:
                    i = str(span).index("img")
                    pass
                except:
                    chars.append(span)
                    pass
            print("SPANS", houseCharSpans)
            print("AFTER", chars)
            
            # make a list with every possible characteristic
            houseCharacteristics = {
                "land": "", 
                "construction": "", 
                "fullbathrooms": "", 
                "parking": "", 
                "bedrooms": "", 
                "halfbathrooms": "", 
                "years": "", 
            }

            return

            # loop through characteristics
            for item in chars:
                
                # clean the string (full of whitespaces, a mess)
                # remove every non-alphanumerican value
                new = re.sub('[^0-9A-Za-zÑñ]', '', item.text)
                print("new", new)

                # TODO: REFACTOR THIS CODE!!
                
                # list every possible house characteristic
                characteristics = ["total", "construido", "baño", "estacionamiento", "recmara", "medio", "antigedad", "aestrenar"]
                actualCharacteristics = ["land", "construction", "fullbathrooms", "parking", "bedrooms", "halfbathrooms", "years", "years"]
                
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
            #"link": houseLink,
            houseData = {
                "name": houseName,
                "price": housePrice,
                "zone": zone,
                "city_hall": city_hall,
                "details": houseCharacteristics
            }            
            db.storeHouseInformation(houseData) if db != None else None
            print(houseData)
            return
