import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time, datetime
from wait import element_has_new_scroll_height

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
    modal = driver.find_element_by_class_name("modal-content")
    match_elems = driver.find_elements_by_class_name('match-history-stats__row')
    for i in range(5):
        last_elem = match_elems[-1]
        scrollHeight = driver.execute_script('return arguments[0].scrollHeight', modal)
        driver.execute_script('arguments[0].scrollIntoView();', last_elem)
        try:
            WebDriverWait(driver, 4).until(element_has_new_scroll_height((By.CLASS_NAME, 'modal-content'), scrollHeight))
        except TimeoutException:
            print("Timed out waiting for scrolled content to load")
        match_elems += last_elem.find_elements_by_xpath('following-sibling::tr')
    print(len(match_elems))
    match_data = []
    for match_elem in match_elems:
        try:
            date_elem = match_elem.find_element_by_xpath(".//td[1]/span")
            result_elem = match_elem.find_element_by_xpath(".//td[3]/div/span")
            score_elem = match_elem.find_element_by_xpath(".//td[4]/div/span")
            map_elem = match_elem.find_element_by_xpath(".//td[5]/div/span")
            match_data.append({
                'date' : datetime.datetime.strptime(date_elem.text+" 2018", "%d %b - %H:%M %Y"),
                'result' : 1 if result_elem.text == "WIN" else 0,
                'score' : score_elem.text,
                'map' : map_elem.text
            })
        except NoSuchElementException:
            continue
    print(match_data)
    driver.quit()


js_parser('https://www.faceit.com/en/players-modal/eXo/stats/csgo')
