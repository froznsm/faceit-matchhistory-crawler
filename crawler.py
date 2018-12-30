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

class Crawler:

    def __init__(self, url):
            self.url = url

    def get_url(self, *args):
        return self.url

    def crawl_matches(self, min_match_date, url = ""):
        if not url:
            url = self.url
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options, executable_path='geckodriver.exe')
        driver.get(url)
        timeout = 15
        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'match-history-stats__row'))
            WebDriverWait(driver, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
            driver.quit()
            exit()

        modal = driver.find_element_by_class_name("modal-content")
        last_elem = driver.find_elements_by_class_name('match-history-stats__row')[-1]
        last_match_time = datetime.datetime.strptime(last_elem.find_element_by_xpath(".//td[1]/span").text+" 2018", "%d %b - %H:%M %Y")
        while last_match_time > min_match_date:
            scrollHeight = driver.execute_script('return arguments[0].scrollHeight', modal)
            driver.execute_script('arguments[0].scrollIntoView();', last_elem)
            try:
                WebDriverWait(driver, timeout).until(element_has_new_scroll_height((By.CLASS_NAME, 'modal-content'), scrollHeight))
            except TimeoutException:
                print("Timed out waiting for scrolled content to load")
                last_date = modal.find_elements_by_class_name('match-history-stats__row')[-1].find_element_by_xpath('.//td[1]/span').text
                print("The oldest match loaded was played on "+ last_date)
                break
            new_elems = last_elem.find_elements_by_xpath('following-sibling::tr')
            if new_elems:
                last_elem = new_elems[-1]
            else:
                print("No new matches found on last scroll")
            last_match_time = datetime.datetime.strptime(last_elem.find_element_by_xpath(".//td[1]/span").text+" 2018", "%d %b - %H:%M %Y")

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        rows = soup.find_all('tr','match-history-stats__row')
        match_data = []
        for match_elem in rows[1:]:
            cells = match_elem.find_all('td')
            date_elem = cells[0].find('span')
            date = datetime.datetime.strptime(date_elem.get_text()+" 2018", "%d %b - %H:%M %Y")
            if date < min_match_date:
                break
            result_elem = cells[2].find('span')
            score_elem = cells[3].find('span')
            map_elem = cells[4].find('span')
            match_data.append({
                'date' : date,
                'result' : 1 if result_elem.get_text() == "WIN" else 0,
                'score' : score_elem.get_text(),
                'map' : map_elem.get_text()
            })
        driver.quit()
        return match_data
