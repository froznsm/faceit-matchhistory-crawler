import datetime
from crawler import Crawler

match_crawler = Crawler('https://www.faceit.com/en/players-modal/eXo/stats/csgo')


matches = match_crawler.crawl_matches(datetime.datetime(2018, 11, 1), 10)

def find_breaks_and_streaks(matches):
    matchtime = datetime.timedelta(hours = 7)
    streaks = []
    streak = datetime.timedelta(0)
    for match1, match2 in zip(matches[0:], matches[1:]):
        delta = match2['date'] - match1['date']
        if delta > matchtime:
            print('Break after the match started at '+match1['date'].strftime('%d %b - %H:%M %Y') +'. It was '+str(delta)+' long.')
            print('Streak was '+str(streak))
            streaks.append(streak)
            streak = datetime.timedelta(0)
        else:
            streak += delta
    print([str(s) for s in sorted(streaks, reverse=True)])


find_breaks_and_streaks(matches)
