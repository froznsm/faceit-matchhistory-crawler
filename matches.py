import datetime
from crawler import Crawler

player_name = 'nooky'

match_crawler = Crawler('https://www.faceit.com/en/players-modal/{}/stats/csgo'.format(player_name))


matches = match_crawler.crawl_matches(datetime.datetime(2018, 11, 1), 10)

def find_breaks_and_streaks(matches):
    matchtime = datetime.timedelta(hours = 7)
    streaks = []
    streak = datetime.timedelta(0)
    streak_start = matches[0]['date']
    for match1, match2 in zip(matches[0:], matches[1:]):
        delta = match2['date'] - match1['date']
        if delta > matchtime:
            break_end = match2['date']
            streak_end = break_start = match1['date'] + datetime.timedelta(minutes = 90)
            streak = streak_end - streak_start
            game_break = break_end - break_start
            streak_string = 'Streak from '+streak_start.strftime('%d %b - %H:%M')+' to '+streak_end.strftime('%d %b - %H:%M')
            streak_duration_string = 'Streak lasted '+str(streak)
            break_string = 'Break from '+break_start.strftime('%d %b - %H:%M')+' to '+break_end.strftime('%d %b - %H:%M')
            break_duration_string = 'Break lasted '+str(game_break)
            print(streak_string, streak_duration_string)
            print(break_string, break_duration_string)
            # print('Break from '+break_start.strftime('%d %b - %H:%M') +' until '+ match2['date'].strftime('%d %b - %H:%M'))
            # print('It was '+str(delta - datetime.timedelta(minutes = 90))+' long.')
            streaks.append(streak)
            streak_start = match2['date']
    print([str(s) for s in sorted(streaks, reverse=True)])


find_breaks_and_streaks(matches)
