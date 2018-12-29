import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

def simple_parser(url):
    code = requests.get(url)
    plain = code.text
    print(plain)
    s = BeautifulSoup(plain, "html.parser")
    for link in s.findAll('div', {'class':'match-history-stats__row'}):
        print('found')

# simple_parser('https://www.faceit.com/en/players-modal/eXo/stats/csgo')


def js_parser(WebUrl):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options, executable_path='geckodriver.exe')
    driver.get(WebUrl)
    timeout = 10
    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'match-history-stats__row'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
        driver.quit()
        exit()

    matches = driver.find_elements_by_class_name('match-history-stats__row')
    print(len(matches))
    for match in matches:
        try:
            date = match.find_element_by_xpath(".//td[1]/span")
            result = match.find_element_by_xpath(".//td[3]/div/span")
        except NoSuchElementException:
            continue
        print('The match on {} was a {}'.format(date.text, result.text))
    driver.quit()



js_parser('https://www.faceit.com/en/players-modal/eXo/stats/csgo')
