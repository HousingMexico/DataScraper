from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

URL = "https://www.inmuebles24.com/inmuebles-en-venta-en-ciudad-de-mexico.html"

options = Options()
options.headless = True
driver = webdriver.Firefox()

driver.get(URL)
soup = BeautifulSoup(driver.page_source, 'html.parser')
prettify = soup.prettify()
print(prettify)
