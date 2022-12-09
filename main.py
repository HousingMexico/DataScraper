from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

URL = "https://www.inmuebles24.com/casas-en-venta-en-ciudad-de-mexico-pagina-"

for page in range(1, 10):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox()

    driver.get(URL + str(page) + '.html')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    property_div = soup.find_all("div", {"class": "sc-ge2uzh-2 hWApJB"})

    filename = 'propiedades.csv'

    for item in property_div:
        print(item.text)
