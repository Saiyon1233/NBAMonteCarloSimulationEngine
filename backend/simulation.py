from game import simulate_game
from season import simulate_season

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