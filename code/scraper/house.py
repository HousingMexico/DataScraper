from bs4 import BeautifulSoup

# URL to fetch information
URL = "https://www.inmuebles24.com/casas-en-venta-en-ciudad-de-mexico-pagina-"

# obtain house information
def get_house_data(scraper):

   # inmuebles24 shows estate on page index
   for page in range(1, 10):

      # obtain the website   
      driver = scraper.get(URL + str(page) + '.html').text

      # parse HTML
      soup = BeautifulSoup(driver, 'html.parser')

      # obtain individual house's div
      property_div = soup.find_all("div", {"class": "sc-ge2uzh-2 hWApJB"})

      # loop through the items
      for item in property_div:
         print(item)
         # propiedades_dict = {"Name": propiedades}