from bs4 import BeautifulSoup
import re

# URL to fetch information
URL = 'https://www.inmuebles24.com/casas-en-venta-en-ciudad-de-mexico-pagina-'

# obtain house information
def get_house_data(scraper, debug, db):

    # inmuebles24 shows estate on page index
    for page in range(1, 5):

        # obtain website where houses are listed (20 houses per page)
        driver = scraper.get(URL + str(page) + '.html').text

        # parse main HTML
        soup = BeautifulSoup(driver, 'html.parser')

        # locate properties (individual divs)
        individualDivs = soup.find_all('div', {"class": "sc-i1odl-0 cYmZqs"})
        # it will extract the link to the individual page of each property

        # loop through each div and obtain each individual house inforation
        for idividualHouse in individualDivs:

            # base URL where the route of the div will be added
            baseURL = 'https://www.inmuebles24.com'

            # data-to-posting is the attribute that contains the link of individual homes
            # link of each individual house 
            houseLink = baseURL + str(idividualHouse['data-to-posting'])
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


            # obtain house information: size, bedrooms, etc
            houseChar = soupInd.find("ul", {"class":"section-icon-features"}).find_all("li") 
            houseCharacteristics = []

            # loop through items
            for item in houseChar:
                
                # clean the string (full of whitespaces, a mess)
                # remove every non-alphanumerican value
                new = re.sub('[^0-9]', '', item.text)

                # append to characteristics array
                houseCharacteristics.append(new)

            # register the house in the database if parameter is True in root's main.py
            houseData = {
                "link": houseLink,
                "name": houseNameH1,
                "price": housePrice,
                "details": houseCharacteristics
            }
            db.storeHouseInformation(houseData) if db != None else None