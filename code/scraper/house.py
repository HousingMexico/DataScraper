from bs4 import BeautifulSoup
import re
import json

# URL to fetch information
URL = 'https://www.inmuebles24.com/'

# obtain house information
def get_house_data(scraper, debug, db, longDescriptions):

    # inmuebles24 shows estate on page index
    for page in range(1, 100):

        print(page)

        # obtain website where houses are listed (20 houses per page)
        driver = scraper.get(URL + 'casas-en-venta-en-ciudad-de-mexico' + '-pagina-' + str(page) + '.html').text
        # parse main HTML
        soup = BeautifulSoup(driver, 'html.parser')

        # obtain specific house links
        links = soup.find_all('a', {"class": "sc-i1odl-12 EWzaP"})

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
            houseNameClean = houseNameH1.replace(" ", "")
            print(f"HOUSENAME: {houseNameH1.strip()}") if debug == True else None
            
            # obtain price (span) inside the div of the price item
            housePrice = soupInd.find("div", {"class":"price-value"}).find("span")

            # remove non-numbers (mainly MXN and numer commas)
            housePrice = re.sub('[^0-9]', '', housePrice.text.strip())
            print(f"HOUSEPRICE: {housePrice}") if debug == True else None 
            
            # Find generalFeatures
            dataSc = soupInd.find("script", text=re.compile('generalFeatures')).string

            groupedData = re.search(r'(\{.*\})', dataSc).group(1)
            jsonData = json.loads(groupedData)

            generalFeatures = jsonData.get('generalFeatures', {})

            # OLD CODE, might be useful
            # generalCharacteristics = generalFeatures.get('Características generales', {})
            # services = generalFeatures.get('Servicios', {})
            # amenidades = generalFeatures.get('Amenidades', {})
            # exteriores = generalFeatures.get('Exteriores', {})

            # for value in generalCharacteristics.values():
            #    label = value.get('label', None)
            #    if label is not None:
            #        print(f"Label: {label}")

            generalCharacteristics = [] 
            services = [] 
            amenidades = [] 
            exteriors = []

            # Will loop through the main categories ("caracteristicas..", "Servicios", etc) and subcategories is the dictionary that contains the subcategoriesc
            for category, subcategories in generalFeatures.items():
                for subcategories, values in subcategories.items():
                    # Subcategories are the ids, and values are label, featureID, etc.
                    label = values.get('label', None)
                    if label is not None:
                        if category == "Características generales":
                            generalCharacteristics.append(label)
                        elif category == "Servicios":
                            services.append(label)
                        elif category == "Amenidades":
                            amenidades.append(label)
                        elif category == "Exteriores":
                            exteriors.append(label)

            print(f"Características generales", generalCharacteristics) if debug == True else None
            print(f"Servicios", services) if debug == True else None
            print(f"Amenidades", amenidades) if debug == True else None
            print(f"Exteriors", exteriors) if debug == True else None

            # Latitude and longitud

            mapImg = soupInd.find("img", {"id": "static-map"})
            print(mapImg)
            src = mapImg.get('src')
            try:
                startOfC = src.find('center=') + len('center')
                endOfC = src.find('&', startOfC)

                coordinates = src[startOfC:endOfC]
                latitude, longitude = coordinates.split('&')[0].split(',')
                latitudeClean = latitude.lstrip('=')
                print("Latitude: ", latitudeClean)
                print("Longitude: ", longitude)
            except:
                latitudeClean = 0
                longitude = 0

            

            # It will find the hgroup attribute and extract the span where the location is located
            try: 
                locationDirty = soupInd.find("div", {"class":"section-location-property"}).find("h4")
                location = str(locationDirty).replace("<h4>", "").replace("</h4>", "")
            except:
                pass

            print(location) if debug == True else None

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
                characteristics = ["tot", "cub", "baños", "estac", "rec", "mediobaño", "mediosbaños", "os", "aestrenar"]
                actualCharacteristics = ["size", "built", "fullbathrooms", "parking", "bedrooms", "halfbathrooms", "halfbathrooms", "years", "years"]

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

            # obtain long house description
            """ if longDescriptions == True:
                descriptionDirty = soupInd.find("div", id="longDescription")
                print(descriptionDirty) """

            # register the house in the database if parameter is True in root's main.py
            houseData = {
                "link": houseLink,
                "name": houseNameClean,
                "price": housePrice,
                "zone": zone,
                "city_hall": city_hall,
                "latitude": latitudeClean,
                "longitude": longitude,
                "details": houseCharacteristics,
                "characteristics": str(generalCharacteristics),
                "amenities": str(amenidades),
                "services": str(services),
                "exteriors": str(exteriors),
            }            
            try:
                db.storeHouseInformation(houseData) if db != None else None
            except:
                pass
           
