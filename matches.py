import datetime
from crawler import Crawler


def find_breaks_and_streaks(matches):
    """Calculate the streaks of continuous playing and the breaks inbetween those streaks.

    matches --  A matchdata list of dictionaries as returned by the Crawler
    return  --  A tuple of lists, one for streaks one for breaks,
                each consisting of 3-tuples with a structure of (start, end, duration)
    """
    if not matches:
        print("no matches")
        return None
    # average time a match will last (consider overtime on faceit)
    average_matchtime = datetime.timedelta(minutes = 90)

    # this duration and upwards is considered to break a streak of continuous playing
    min_time_for_break = datetime.timedelta(hours = 5, minutes = 30)

    streaks = []
    breaks = []
    streak_start = matches[0]['date']

    # compare each match with the next and check whether the time in between breaks the streak
    for match1, match2 in zip(matches[0:], matches[1:]):
        delta = match2['date'] - (match1['date'] + average_matchtime)
        if delta > min_time_for_break:
            # assign streak and break ends and beginnings
            break_end = match2['date']
            streak_end = break_start = match1['date'] + average_matchtime
            streak_duration = streak_end - streak_start
            break_duration = break_end - break_start

            # create output strings and print them
            streak_string = 'Streak from '+streak_start.strftime('%d %b - %H:%M')+' to '+streak_end.strftime('%d %b - %H:%M')
            streak_duration_string = 'Streak lasted '+str(streak_duration)
            break_string = 'Break from '+break_start.strftime('%d %b - %H:%M')+' to '+break_end.strftime('%d %b - %H:%M')
            break_duration_string = 'Break lasted '+str(break_duration)
            # print(streak_string, streak_duration_string)
            # print(break_string, break_duration_string)

            # append streaks and breaks to corresponding lists
            streak = (streak_start, streak_end, streak_duration)
            streaks.append(streak)
            breake = (break_start, break_end, break_duration)
            breaks.append(break_duration)

            # reset the startdate of the next streak
            streak_start = match2['date']
    return (streaks, breaks)

def winrate(matches):
    """Calculate the winrate of the given matches

    matches --  A matchdata list of dictionaries as returned by the crawler

    return  --  A percentage
    """
    if not matches:
        print('no matches')
        return None

    win_loss = [match['result'] for match in matches]
    return sum(win_loss)/len(win_loss)


def maps(matches):
    """Calculate the number of wins and losses and winrate mapwise.

    matches --  A matchdata list of dictionaries as returned by the crawler

    returns --  A dictionary of the maps with a 3-tuple of wins/losses/winrate for each
    """
    if not matches:
        print('no matches')
        return None

    maps = {}
    for match in matches:
        map = match['map']
        score = match['score']
        result = match['result']
        # add map to dictionary
        if not map in maps:
            maps[map] = {'wins': 0, 'losses': 0, 'winrate': 0.0}
        map_data = maps[map]
        if result:
            map_data['wins'] += 1
        else:
            map_data['losses'] += 1
        matches_played = map_data['wins'] + map_data['losses']

        # compute moving average on winrate
        map_data['winrate'] = map_data['winrate'] + (result - map_data['winrate']) / matches_played
    return maps

# name of the profile to crawl
player_name = 'nooky'
# date from which to now matches will be in the list
min_date = datetime.datetime(2018, 12, 1)

# initalise crawler with url
match_crawler = Crawler('https://www.faceit.com/en/players-modal/{}/stats/csgo'.format(player_name))

# call the crawler with the date
matches = match_crawler.crawl_matches(min_date, 10)

winrate = winrate(matches)
print('{0:} played {1:} matches from {2:} until now'.format(player_name, len(matches), matches[0]['date'].strftime("%B %d, %Y")))
print('The winrate was {:.2%}'.format(winrate))

# output longest continuous time playing
streaks, breaks = find_breaks_and_streaks(matches)
longest_streak = max(streaks, key=lambda x: x[2])[2]
print('The longest continuous time {} played for was: '.format(player_name)+str(longest_streak))

maps = maps(matches)
for key in maps.keys():
    print("%s: %s" % (key, maps[key]))
