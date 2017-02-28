import pandas

def group_by_team(team_file, game_results_file, game_type):
	teams = pandas.read_csv(team_file, sep=',', header=0)
	records = pandas.read_csv(game_results_file, sep=',', header=0)
	
	for _, row in teams.iterrows():
		team_id = row['Team_Id']
		team_records = records.loc[(records['Wteam'] == team_id) | (records['Lteam'] == team_id)]
		team_records.to_csv('data/team_record/%d_%s.csv' % (team_id, game_type), sep=',',
							columns=list(records.columns.values), index=False)

if __name__=='__main__':
	group_by_team('data/Teams.csv', 'data/RegularSeasonDetailedResults.csv', 'reg')
	group_by_team('data/Teams.csv', 'data/TourneyDetailedResults.csv', 'tourney')