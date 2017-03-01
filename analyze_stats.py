import pandas
import matplotlib.pyplot as plt
import os

def analyze_seasons(infile):
    team_id = int(os.path.split(infile)[1][:4])
    print(team_id)
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
        
if __name__ == '__main__':
    analyze_seasons('data/team_record/1417_reg.csv')
