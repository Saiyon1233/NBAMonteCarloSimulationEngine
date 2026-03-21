from nba_api.stats.endpoints import LeagueDashTeamStats
import pandas as pd
import numpy as np
    
def fetch_team_data(season):
    team_stats = LeagueDashTeamStats(season=season, measure_type_detailed_defense="Advanced")
    df = team_stats.get_data_frames()[0]
    
    league_average = df['OFF_RATING'].mean()
    
    data = {}
    for _, row in df.iterrows():
        team_name = row["TEAM_NAME"]
        offensive_rating = row['OFF_RATING']
        defensive_rating = row['DEF_RATING']
        data[team_name] = {"offense": offensive_rating, "defense": defensive_rating}
    
    return data, league_average

def normalize_team_name(name, data):
    name_lower = name.lower()

    for team in data.keys():
        if team.lower() == name_lower:
            return team

    return None

def expected_score(team_a, team_b, data, league_average):
    team_a_key = normalize_team_name(team_a, data)
    team_b_key = normalize_team_name(team_b, data)

    if not team_a_key:
        raise ValueError(f"Team '{team_a}' not found")
    if not team_b_key:
        raise ValueError(f"Team '{team_b}' not found")

    or_a = data[team_a_key]["offense"]
    dr_b = data[team_b_key]["defense"]

    or_b = data[team_b_key]["offense"]
    dr_a = data[team_a_key]["defense"]

    score_a = (or_a * dr_b) / league_average
    score_b = (or_b * dr_a) / league_average

    return score_a, score_b
