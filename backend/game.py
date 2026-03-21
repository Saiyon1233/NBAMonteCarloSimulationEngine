import numpy as np
from model import expected_score

def simulate_game(team_a, team_b, data):
    exp_a, exp_b = expected_score(team_a, team_b, data, data["league_average"])
    
    # Add randomness
    score_a = np.random.normal(exp_a, 12)
    score_b = np.random.normal(exp_b, 12)
    
    score_a = int(round(score_a))
    score_b = int(round(score_b))
    
    # No ties in NBA
    while score_a == score_b:
        score_a += np.random.randint(1, 5)
        score_b += np.random.randint(1, 5)
    
    winner = team_a if score_a > score_b else team_b
    
    return {
        "team_a": team_a,
        "team_b": team_b,
        "score_a": score_a,
        "score_b": score_b,
        "winner": winner
    }
