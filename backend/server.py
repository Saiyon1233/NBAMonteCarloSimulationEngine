from flask import Flask, request, jsonify
from model import load_data
from game import simulate_game

app = Flask(__name__)
    
data, league_average = load_data()
data["league_average"] = league_average
    
@app.route('/simulate', methods=['POST'])
def simulate():
    req_data = request.get_json()
    team_a = req_data['team_a']
    team_b = req_data['team_b']
        
    score_a, score_b = simulate_game(team_a, team_b, data)
        
    return jsonify({"team_a_score": score_a, "team_b_score": score_b})
    
if __name__ == '__main__':
    app.run(port=5000, debug=True)