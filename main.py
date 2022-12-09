from bs4 import BeautifulSoup
import pandas as pd
import cloudscraper

URL = "https://www.inmuebles24.com/casas-en-venta-en-ciudad-de-mexico-pagina-"

for page in range(1, 10):
    scraper = cloudscraper.create_scraper()
    driver = scraper.get(URL + str(page) + '.html').text
    soup = BeautifulSoup(driver, 'html.parser')
    property_div = soup.find_all("div", {"class": "sc-ge2uzh-2 hWApJB"})

    propiedades = []

    for propiedad in property_div:
        propiedades.append(propiedad)
        print(propiedad)

    propiedades_dict = {"Name": propiedades}

    df = pd.DataFrame(propiedades_dict)

    save_to_csv = df.to_csv('RealState.csv', index=True)
