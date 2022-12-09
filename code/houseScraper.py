from bs4 import BeautifulSoup

URL = "https://www.inmuebles24.com/casas-en-venta-en-ciudad-de-mexico-pagina-"


def get_house_data(scraper):
    for page in range(1, 10):
        driver = scraper.get(URL + str(page) + '.html').text
        soup = BeautifulSoup(driver, 'html.parser')
        property_div = soup.find_all("div", {"class": "sc-ge2uzh-2 hWApJB"})
        for item in property_div:
            print(item)
#         propiedades_dict = {"Name": propiedades}
