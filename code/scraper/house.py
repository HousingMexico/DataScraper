from bs4 import BeautifulSoup

# URL to fetch information
URL = 'https://www.inmuebles24.com/casas-en-venta-en-ciudad-de-mexico-pagina-'

# obtain house information
def get_house_data(scraper):

   # inmuebles24 shows estate on page index
   for page in range(1, 10):

      # obtain the website   
      driver = scraper.get(URL + str(page) + '.html').text

      # parse HTML
      soup = BeautifulSoup(driver, 'html.parser')

      # get all divs with the location of each house
      houseNameDiv = soup.find_all("div", {"class": "sc-ge2uzh-2 hWApJB"})

      # Loop through all the divs and only retrieve the text without the tag
      for div in houseNameDiv:
         print(div.text)

      # It will find the divs of each property
      individualPage = soup.find_all('div',{"class": "sc-i1odl-0 cYmZqs"})

      # It will extract the link to the individual page of each property
      # In Inmuebles 24, data-to-posting is the attribute that contains the route to the individual page
      for indPage in individualPage:
          baseURL = 'https://www.inmuebles24.com'
          print(indPage['data-to-posting'])
          driverInd = scraper.get(baseURL + str(indPage['data-to-posting'])).text
          soupInd = BeautifulSoup(driverInd, 'html.parser')
