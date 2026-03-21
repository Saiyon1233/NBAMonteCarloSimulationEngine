import traceback
from flask import Flask, request, jsonify
from simulation import monte_carlo_simulation
from model import fetch_team_data
from game import simulate_game
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

today = pd.to_datetime("today")

if today.month >= 10:
    season = f"{today.year}-{str(today.year + 1)[-2:]}"
else:    
    season = f"{today.year - 1}-{str(today.year)[-2:]}"

data, league_average = fetch_team_data(season)
data["league_average"] = league_average
    
@app.route('/')
def home():
    return "NBA Monte Carlo API is running" 
    
@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        req = request.get_json()

        team_a = req.get("team1")
        team_b = req.get("team2")

        results = monte_carlo_simulation(team_a, team_b, data)

        total = results["team_a_wins"] + results["team_b_wins"]

        prob_a = results["team_a_wins"] / total
        prob_b = results["team_b_wins"] / total

        winner = team_a if prob_a > prob_b else team_b

        return jsonify({
            "winner": winner,
            "team_a_win_probability": prob_a,
            "team_b_win_probability": prob_b,
            "avg_score_a": results["avg_score_a"],
            "avg_score_b": results["avg_score_b"]
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)