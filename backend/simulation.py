from game import simulate_game


def monte_carlo_simulation(team_a, team_b, data, iterations=10000):
    results = {
        "team_a_wins": 0,
        "team_b_wins": 0,
        "team_a_points": 0,
        "team_b_points": 0
    }
    
    for _ in range(iterations):
        game = simulate_game(team_a, team_b, data)

        score_a = game["score_a"]
        score_b = game["score_b"]

        results["team_a_points"] += score_a
        results["team_b_points"] += score_b
        
        if score_a > score_b:
            results["team_a_wins"] += 1
        else:
            results["team_b_wins"] += 1

    results["avg_score_a"] = results["team_a_points"] / iterations
    results["avg_score_b"] = results["team_b_points"] / iterations

    return results