import datetime
from crawler import Crawler

player_name = 'nooky'

match_crawler = Crawler('https://www.faceit.com/en/players-modal/{}/stats/csgo'.format(player_name))


matches = match_crawler.crawl_matches(datetime.datetime(2018, 11, 1), 10)

def find_breaks_and_streaks(matches):
    matchtime = datetime.timedelta(hours = 7)
    streaks = []
    breaks = []
    streak_duration = datetime.timedelta(0)
    streak_start = matches[0]['date']
    for match1, match2 in zip(matches[0:], matches[1:]):
        delta = match2['date'] - match1['date']
        if delta > matchtime:
            break_end = match2['date']
            streak_end = break_start = match1['date'] + datetime.timedelta(minutes = 90)
            streak_duration = streak_end - streak_start
            break_duration = break_end - break_start
            streak_string = 'Streak from '+streak_start.strftime('%d %b - %H:%M')+' to '+streak_end.strftime('%d %b - %H:%M')
            streak_duration_string = 'Streak lasted '+str(streak_duration)
            break_string = 'Break from '+break_start.strftime('%d %b - %H:%M')+' to '+break_end.strftime('%d %b - %H:%M')
            break_duration_string = 'Break lasted '+str(break_duration)
            print(streak_string, streak_duration_string)
            print(break_string, break_duration_string)
            streak = (streak_start, streak_end, streak_duration)
            streaks.append(streak)
            breake = (break_start, break_end, break_duration)
            breaks.append(breake_duration)
            streak_start = match2['date']
    return (streaks, breaks)


find_breaks_and_streaks(matches)
