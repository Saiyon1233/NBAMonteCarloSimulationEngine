from game import simulate_game
from season import simulate_season
from playoffs import simulate_playoffs, simulate_series

def monte_carlo_game_simulation(team_a, team_b, data, league_average, iterations=10000):
    results = {
        "team_a_wins": 0,
        "team_b_wins": 0,
        "team_a_points": 0,
        "team_b_points": 0
    }
    
    iterations = int(iterations)
    
    for _ in range(iterations):
        game = simulate_game(team_a, team_b, data, league_average)

        score_a = game["score_a"]
        score_b = game["score_b"]

        results["team_a_points"] += score_a
        results["team_b_points"] += score_b
        
        if score_a > score_b:
            results["team_a_wins"] += 1
        else:
            results["team_b_wins"] += 1

    results["avg_score_a"] = int(round(results["team_a_points"] / iterations, 0))
    results["avg_score_b"] = int(round(results["team_b_points"] / iterations, 0))

    return results

def monte_carlo_season_simulation(teams, data, league_average, iterations=10000):
    
    season_results = {
        team: {
            "wins": 0,
            "losses": 0,
            "conference": ""
        }
        for team in teams
    }
    
    iterations = int(iterations)
    
    for _ in range(iterations):
         results = simulate_season(teams, data, league_average)
         for team in teams:
             # Extract this team's wins and losses from the iteration results
             wins = results["wins"][team]
             loss = results["loss"][team]
             # Accumulate across all iterations
             season_results[team]["wins"] += wins
             season_results[team]["losses"] += loss
             # Store conference (same for all iterations)
             season_results[team]["conference"] = results["conference"].get(team, "Unknown")

    # Average the accumulated wins/losses across all iterations
    season_results = {team: {"wins": int(round(season_results[team]["wins"] / iterations)),
                             "losses": int(round(season_results[team]["losses"] / iterations)),
                             "conference": season_results[team]["conference"]} for team in teams}
    
    return season_results

def monte_carlo_playoffs_simulation(teams, season_results, data, league_average, iterations=10000):
    """Simulate playoffs multiple times and return detailed bracket with aggregated results."""
    # Track aggregated bracket data across iterations
    playoff_bracket = {
        "first_round": {"east": {}, "west": {}},
        "second_round": {"east": {}, "west": {}},
        "conference_finals": {"east": {}, "west": {}},
        "nba_finals": {},
        "championships": {team: 0 for team in teams},
        "finals_appearances": {team: 0 for team in teams},
        "conference_championships": {team: 0 for team in teams}
    }
    
    iterations = int(iterations)
    
    for _ in range(iterations):
        bracket = simulate_playoffs(teams, season_results, data, league_average)
        
        # Aggregate first round results
        for i, matchup in enumerate(bracket["first_round"]["east"]):
            if i not in playoff_bracket["first_round"]["east"]:
                playoff_bracket["first_round"]["east"][i] = {"matchup": matchup["matchup"], "winner_count": {}, "total_games": 0}
            winner = matchup["winner"]
            playoff_bracket["first_round"]["east"][i]["winner_count"][winner] = playoff_bracket["first_round"]["east"][i]["winner_count"].get(winner, 0) + 1
            playoff_bracket["first_round"]["east"][i]["total_games"] += matchup["games"]
        
        for i, matchup in enumerate(bracket["first_round"]["west"]):
            if i not in playoff_bracket["first_round"]["west"]:
                playoff_bracket["first_round"]["west"][i] = {"matchup": matchup["matchup"], "winner_count": {}, "total_games": 0}
            winner = matchup["winner"]
            playoff_bracket["first_round"]["west"][i]["winner_count"][winner] = playoff_bracket["first_round"]["west"][i]["winner_count"].get(winner, 0) + 1
            playoff_bracket["first_round"]["west"][i]["total_games"] += matchup["games"]
        
        # Aggregate second round results
        for i, matchup in enumerate(bracket["second_round"]["east"]):
            if i not in playoff_bracket["second_round"]["east"]:
                playoff_bracket["second_round"]["east"][i] = {"matchup": matchup["matchup"], "winner_count": {}, "total_games": 0}
            winner = matchup["winner"]
            playoff_bracket["second_round"]["east"][i]["winner_count"][winner] = playoff_bracket["second_round"]["east"][i]["winner_count"].get(winner, 0) + 1
            playoff_bracket["second_round"]["east"][i]["total_games"] += matchup["games"]
        
        for i, matchup in enumerate(bracket["second_round"]["west"]):
            if i not in playoff_bracket["second_round"]["west"]:
                playoff_bracket["second_round"]["west"][i] = {"matchup": matchup["matchup"], "winner_count": {}, "total_games": 0}
            winner = matchup["winner"]
            playoff_bracket["second_round"]["west"][i]["winner_count"][winner] = playoff_bracket["second_round"]["west"][i]["winner_count"].get(winner, 0) + 1
            playoff_bracket["second_round"]["west"][i]["total_games"] += matchup["games"]
        
        # Aggregate conference finals
        east_final = bracket["conference_finals"]["east"]
        if "east" not in playoff_bracket["conference_finals"] or playoff_bracket["conference_finals"]["east"] == {}:
            playoff_bracket["conference_finals"]["east"] = {"matchup": east_final["matchup"], "winner_count": {}, "total_games": 0}
        playoff_bracket["conference_finals"]["east"]["winner_count"][east_final["winner"]] = playoff_bracket["conference_finals"]["east"]["winner_count"].get(east_final["winner"], 0) + 1
        playoff_bracket["conference_finals"]["east"]["total_games"] += east_final["games"]
        
        west_final = bracket["conference_finals"]["west"]
        if "west" not in playoff_bracket["conference_finals"] or playoff_bracket["conference_finals"]["west"] == {}:
            playoff_bracket["conference_finals"]["west"] = {"matchup": west_final["matchup"], "winner_count": {}, "total_games": 0}
        playoff_bracket["conference_finals"]["west"]["winner_count"][west_final["winner"]] = playoff_bracket["conference_finals"]["west"]["winner_count"].get(west_final["winner"], 0) + 1
        playoff_bracket["conference_finals"]["west"]["total_games"] += west_final["games"]
        
        # Aggregate NBA Finals
        nba_final = bracket["nba_finals"]
        if "matchup" not in playoff_bracket["nba_finals"]:
            playoff_bracket["nba_finals"] = {"matchup": nba_final["matchup"], "winner_count": {}, "total_games": 0}
        playoff_bracket["nba_finals"]["winner_count"][nba_final["winner"]] = playoff_bracket["nba_finals"]["winner_count"].get(nba_final["winner"], 0) + 1
        playoff_bracket["nba_finals"]["total_games"] += nba_final["games"]
        
        # Track championships
        nba_champion = bracket["nba_champion"]
        east_champ = bracket["conference_finals"]["east"]["winner"]
        west_champ = bracket["conference_finals"]["west"]["winner"]
        
        playoff_bracket["championships"][nba_champion] += 1
        playoff_bracket["conference_championships"][east_champ] += 1
        playoff_bracket["conference_championships"][west_champ] += 1
        playoff_bracket["finals_appearances"][east_champ] += 1
        playoff_bracket["finals_appearances"][west_champ] += 1
    
    # Average results
    playoff_bracket["championships"] = {team: playoff_bracket["championships"][team] // iterations for team in teams}
    playoff_bracket["finals_appearances"] = {team: playoff_bracket["finals_appearances"][team] // iterations for team in teams}
    playoff_bracket["conference_championships"] = {team: playoff_bracket["conference_championships"][team] // iterations for team in teams}
    
    return playoff_bracket