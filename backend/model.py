from nba_api.stats.endpoints import LeagueDashTeamStats
import pandas as pd
import numpy as np

datetime = pd.to_datetime("today").strftime("%Y-%m-%d")

if datetime.month >= 10:
    season = f"{datetime.year}-{str(datetime.year + 1)[-2:]}"
else:    
    season = f"{datetime.year - 1}-{str(datetime.year)[-2:]}"
    
def fetch_team_data(season):
    team_stats = LeagueDashTeamStats(season=season)
    df = team_stats.get_data_frames()[0]
    
    league_average = df["OFF_RATING"].mean()
    
    data = {}
    for _, row in df.iterrows():
        team_name = row["TEAM_NAME"]
        offense = row["OFF_RATING"]
        defense = row["DEF_RATING"]
        data[team_name] = {"offense": offense, "defense": defense}
    
    return data, league_average

def expected_score(team_a, team_b, data, league_average):
    or_a = data[team_a]["offense"]
    dr_b = data[team_b]["defense"]
    
    or_b = data[team_b]["offense"]
    dr_a = data[team_a]["defense"]
    
    score_a = (or_a * dr_b) / league_average
    score_b = (or_b * dr_a) / league_average
    
    return score_a, score_b
