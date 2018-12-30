import datetime
from crawler import Crawler

match_crawler = Crawler('https://www.faceit.com/en/players-modal/eXo/stats/csgo')


print(match_crawler.crawl_matches(datetime.datetime(2018, 12, 1)))
