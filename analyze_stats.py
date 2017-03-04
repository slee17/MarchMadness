import pandas
import matplotlib.pyplot as plt
import os
from datetime import date, datetime

TEAM_DATA_LOC = 'data/team_record/'

def analyze_seasons(infile):
    team_id = int(os.path.split(infile)[1][:4])
    team_results = pandas.read_csv(infile)
    current_season, wins = team_results['Season'][0], [0]
    for _, row in team_results.iterrows():
        if row['Season'] != current_season:
            plt.plot(range(len(wins)), wins)
            current_season = row['Season']
            wins = [0]
        elif row['Wteam'] == team_id:
            wins.append(wins[-1] + 1)
        elif row['Lteam'] == team_id:
            wins.append(wins[-1])
    plt.show()

def stats_of_team_to_date(team, date_of_interest):
    team_data = pandas.read_csv(TEAM_DATA_LOC + str(team) + '_reg.csv')
    seasons_data = pandas.read_csv('data/Seasons.csv')
    season_year = date_of_interest.year if date_of_interest.month < 6 else date_of_interest.year + 1
    season_of_interest = seasons_data.loc[seasons_data['Season'] == season_year]
    #print(season_of_interest)
    season_day_zero = datetime.strptime(season_of_interest['Dayzero'].values[0], '%m/%d/%Y')
    day_interest_num = (date_of_interest - season_day_zero).days
    #print(season_day_zero, day_interest_num)

    relevant_games = team_data.loc[(team_data['Season'] == season_year) & (team_data['Daynum'] < day_interest_num)]

    #print(relevant_games)
    stats_to_analyze = ['score', 'fgm','fga','fgm3','fga3','ftm','fta','or','dr','ast','to','stl','blk','pf']
    full_stats = pandas.DataFrame(columns = ['Daynum', 'won', 'loc']+['self '+x for x in stats_to_analyze] + ['opponent ' + x for x in stats_to_analyze])
    for _, row in relevant_games.iterrows():
        stats = {'Daynum':row['Daynum']}
        if int(row['Wteam']) == team:
            prefix, opPrefix = 'W', 'L'
            stats['won'] = 1
            stats['loc'] = row['Wloc']
        elif int(row['Lteam']) == team:
            prefix, opPrefix = 'L', 'W'
            stats['won'] = 0
            # loc = opposite of Wloc if the team lost
            if row['Wloc'] == 'A':
                stats['loc'] = 'H'
            elif row['Wloc'] == 'H':
                stats['loc'] = 'A'
            else:
                stats['loc'] = row['Wloc']
        else:
            print("ERROR, TEAM NOT INVOLVED IN GAME", row)

        for stat in stats_to_analyze:
            stats['self ' + stat] = row[prefix + stat]
            stats['opponent ' + stat] = row[opPrefix + stat]
        full_stats = full_stats.append(stats, ignore_index=True)
    print(full_stats)
    
if __name__ == '__main__':
    stats_of_team_to_date(1417, datetime(2007, 12, 5))
    #analyze_seasons('data/team_record/1417_reg.csv')
