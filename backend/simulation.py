
from backend.game import simulate_game


def monte_carlo_simulation(team_a, team_b, data, iterations=10000):
    results = {"team_a_wins": 0, "team_b_wins": 0}
    
    for _ in range(iterations):
        score_a, score_b = simulate_game(team_a, team_b, data)
        
        if score_a > score_b:
            results["team_a_wins"] += 1
        else:
            results["team_b_wins"] += 1
            
    return results