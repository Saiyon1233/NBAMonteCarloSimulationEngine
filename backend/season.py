from game import simulate_game
import pandas as pd
import numpy as np

def simulate_season(teams, data, league_average):
    wins = {team: 0 for team in teams}
    loss = {team: 0 for team in teams}
    
    TEAM_CONFERENCE_DIVISION = {
        "Atlanta Hawks": {"conference": "East", "division": "Southeast"},
        "Boston Celtics": {"conference": "East", "division": "Atlantic"},
        "Brooklyn Nets": {"conference": "East", "division": "Atlantic"},
        "Charlotte Hornets": {"conference": "East", "division": "Southeast"},
        "Chicago Bulls": {"conference": "East", "division": "Central"},
        "Cleveland Cavaliers": {"conference": "East", "division": "Central"},
        "Detroit Pistons": {"conference": "East", "division": "Central"},
        "Indiana Pacers": {"conference": "East", "division": "Central"},
        "Miami Heat": {"conference": "East", "division": "Southeast"},
        "Milwaukee Bucks": {"conference": "East", "division": "Central"},
        "New York Knicks": {"conference": "East", "division": "Atlantic"},
        "Orlando Magic": {"conference": "East", "division": "Southeast"},
        "Philadelphia 76ers": {"conference": "East", "division": "Atlantic"},
        "Toronto Raptors": {"conference": "East", "division": "Atlantic"},
        "Washington Wizards": {"conference": "East", "division": "Southeast"},
        "Dallas Mavericks": {"conference": "West", "division": "Southwest"},
        "Denver Nuggets": {"conference": "West", "division": "Northwest"},
        "Golden State Warriors": {"conference": "West", "division": "Pacific"},
        "Houston Rockets": {"conference": "West", "division": "Southwest"},
        "LA Clippers": {"conference": "West", "division": "Pacific"},
        "Los Angeles Lakers": {"conference": "West", "division": "Pacific"},
        "Memphis Grizzlies": {"conference": "West", "division": "Southwest"},
        "Minnesota Timberwolves": {"conference": "West", "division": "Northwest"},
        "New Orleans Pelicans": {"conference": "West", "division": "Southwest"},
        "Oklahoma City Thunder": {"conference": "West", "division": "Northwest"},
        "Phoenix Suns": {"conference": "West", "division": "Pacific"},
        "Portland Trail Blazers": {"conference": "West", "division": "Northwest"},
        "Sacramento Kings": {"conference": "West", "division": "Pacific"},
        "San Antonio Spurs": {"conference": "West", "division": "Southwest"},
        "Utah Jazz": {"conference": "West", "division": "Northwest"},
    }
    
    for team in teams:
        schedule = {}
        
        team_conf = TEAM_CONFERENCE_DIVISION[team]["conference"]
        team_div = TEAM_CONFERENCE_DIVISION[team]["division"]
        
        # Build opponents list
        division_opponents = []
        non_div_conf_opponents = []
        non_conf_opponents = []
        
        for other_team in teams:
            if team == other_team:
                continue
                
            other_conf = TEAM_CONFERENCE_DIVISION[other_team]["conference"]
            other_div = TEAM_CONFERENCE_DIVISION[other_team]["division"]
            
            # Classify opponent
            if other_div == team_div:  # Same division
                division_opponents.append(other_team)
            elif other_conf == team_conf:  # Non-division conference
                non_div_conf_opponents.append(other_team)
            else:  # Non-conference
                non_conf_opponents.append(other_team)
        
        # Build schedule: 4 games vs division (3 teams), 4 games vs non-div conference (10 teams), 2 games vs non-conference (15 teams)
        # 12 + 40 + 30 = 82 games total
        for opp in division_opponents:
            schedule[opp] = 4
        for opp in non_div_conf_opponents:
            schedule[opp] = 4
        for opp in non_conf_opponents:
            schedule[opp] = 2
        
        # Simulate games based on the schedule
        for opponent, games in schedule.items():
            for _ in range(games):
                result = simulate_game(team, opponent, data, league_average)

                if result['winner'] == team:
                    wins[team] += 1
                else:
                    loss[team] += 1

    
    return {
        "wins": wins,
        "loss": loss,
        "conference": {
            team: TEAM_CONFERENCE_DIVISION.get(team, {}).get("conference", "Unknown")
            for team in teams
        }
    }