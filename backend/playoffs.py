from game import simulate_game

def simulate_series(team_a, team_b, data, league_average):

    wins_a = 0
    wins_b = 0
    games_played = 0
    
    while wins_a < 4 and wins_b < 4:
        result = simulate_game(team_a, team_b, data, league_average)
        games_played += 1
        
        if result['winner'] == team_a:
            wins_a += 1
        else:
            wins_b += 1
    
    winner = team_a if wins_a == 4 else team_b
    return winner, games_played

def simulate_playoffs(teams, season_results, data, league_average):
    
    # Extract the top 8 teams from each conference based on wins
    east_teams = sorted([(team, season_results[team]["wins"]) for team in season_results if season_results[team]["conference"] == "East"], key=lambda x: x[1], reverse=True)[:8]
    west_teams = sorted([(team, season_results[team]["wins"]) for team in season_results if season_results[team]["conference"] == "West"], key=lambda x: x[1], reverse=True)[:8]
    
    # Initialize bracket structure
    bracket = {
        "first_round": {
            "east": [],
            "west": []
        },
        "second_round": {
            "east": [],
            "west": []
        },
        "conference_finals": {
            "east": [],
            "west": []
        },
        "nba_finals": [],
        "nba_champion": None
    }
    
    # Simulate first round - top 8 seeds in each conference
    # Matchups: 1vs8, 2vs7, 3vs6, 4vs5
    east_first_round_winners = []
    west_first_round_winners = []
    
    for i in range(4):
        # East matchups
        team_a, seed_a = east_teams[i]
        team_b, seed_b = east_teams[7 - i]
        winner, games = simulate_series(team_a, team_b, data, league_average)
        
        bracket["first_round"]["east"].append({
            "matchup": f"{i+1}. {team_a} vs {8-i}. {team_b}",
            "team1": team_a,
            "team2": team_b,
            "winner": winner,
            "games": games
        })
        east_first_round_winners.append(winner)
        
        # West matchups
        team_a, seed_a = west_teams[i]
        team_b, seed_b = west_teams[7 - i]
        winner, games = simulate_series(team_a, team_b, data, league_average)
        
        bracket["first_round"]["west"].append({
            "matchup": f"{i+1}. {team_a} vs {8-i}. {team_b}",
            "team1": team_a,
            "team2": team_b,
            "winner": winner,
            "games": games
        })
        west_first_round_winners.append(winner)
    
    # Simulate second round
    east_second_round_winners = []
    west_second_round_winners = []
    
    for i in range(2):
        # East second round: 1st vs 4th winner, 2nd vs 3rd winner
        team_a = east_first_round_winners[i]
        team_b = east_first_round_winners[3 - i]
        winner, games = simulate_series(team_a, team_b, data, league_average)
        
        bracket["second_round"]["east"].append({
            "matchup": f"{team_a} vs {team_b}",
            "team1": team_a,
            "team2": team_b,
            "winner": winner,
            "games": games
        })
        east_second_round_winners.append(winner)
        
        # West second round
        team_a = west_first_round_winners[i]
        team_b = west_first_round_winners[3 - i]
        winner, games = simulate_series(team_a, team_b, data, league_average)
        
        bracket["second_round"]["west"].append({
            "matchup": f"{team_a} vs {team_b}",
            "team1": team_a,
            "team2": team_b,
            "winner": winner,
            "games": games
        })
        west_second_round_winners.append(winner)
    
    # Simulate Conference Finals
    east_finalist_a = east_second_round_winners[0]
    east_finalist_b = east_second_round_winners[1]
    east_champion, games = simulate_series(east_finalist_a, east_finalist_b, data, league_average)
    bracket["conference_finals"]["east"] = {
        "matchup": f"{east_finalist_a} vs {east_finalist_b}",
        "team1": east_finalist_a,
        "team2": east_finalist_b,
        "winner": east_champion,
        "games": games
    }
    
    west_finalist_a = west_second_round_winners[0]
    west_finalist_b = west_second_round_winners[1]
    west_champion, games = simulate_series(west_finalist_a, west_finalist_b, data, league_average)
    bracket["conference_finals"]["west"] = {
        "matchup": f"{west_finalist_a} vs {west_finalist_b}",
        "team1": west_finalist_a,
        "team2": west_finalist_b,
        "winner": west_champion,
        "games": games
    }
    
    # Simulate NBA Finals
    nba_champion, games = simulate_series(east_champion, west_champion, data, league_average)
    bracket["nba_finals"] = {
        "matchup": f"{east_champion} vs {west_champion}",
        "team1": east_champion,
        "team2": west_champion,
        "winner": nba_champion,
        "games": games
    }
    bracket["nba_champion"] = nba_champion
    
    return bracket