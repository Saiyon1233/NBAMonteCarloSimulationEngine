import React, { useState } from "react";
import axios from "axios";

function App() {
  const [mode, setMode] = useState("game");

  const [team1, setTeam1] = useState("");
  const [team2, setTeam2] = useState("");

  const [result, setResult] = useState(null);
  const [seasonData, setSeasonData] = useState([]); // ✅ FIXED

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Game simulation
  const handleSimulate = async () => {
    if (!team1 || !team2) {
      setError("Please enter both team names");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await axios.post("http://127.0.0.1:5000/simulate", {
        team1,
        team2,
      });

      setResult(response.data);
    } catch (err) {
      console.error(err);
      if (err.response) {
        setError(err.response.data.error || "Backend error");
      } else {
        setError("No response from backend");
      }
    }

    setLoading(false);
  };

  // Season simulation
  const handleSeasonSimulate = async () => {
    setLoading(true);
    setError("");
    setSeasonData([]);

    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/simulate_season"
      );

      // ✅ SAFE HANDLING
      if (Array.isArray(response.data)) {
        setSeasonData(response.data);
      } else if (response.data.standings) {
        setSeasonData(response.data.standings);
      } else {
        setSeasonData([]);
      }
    } catch (err) {
      console.error(err);
      setError("Failed to simulate season");
    }

    setLoading(false);
  };

  // Split + sort standings
  let east = [];
  let west = [];

  if (Array.isArray(seasonData)) {
    east = seasonData
      .filter((t) => t.conference === "East")
      .sort((a, b) => b.wins - a.wins);

    west = seasonData
      .filter((t) => t.conference === "West")
      .sort((a, b) => b.wins - a.wins);
  }

  // Styles
  const containerStyle = {
    minHeight: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "linear-gradient(135deg, #0f172a, #1e293b)",
    color: "white",
    fontFamily: "Arial",
  };

  const cardStyle = {
    background: "#111827",
    padding: "30px",
    borderRadius: "12px",
    width: "400px",
    boxShadow: "0 10px 25px rgba(0,0,0,0.5)",
  };

  const inputStyle = {
    width: "100%",
    padding: "10px",
    marginBottom: "10px",
    borderRadius: "6px",
    border: "none",
    outline: "none",
    fontSize: "14px",
  };

  const buttonStyle = {
    width: "100%",
    padding: "10px",
    borderRadius: "6px",
    border: "none",
    background: loading ? "#6b7280" : "#3b82f6",
    color: "white",
    fontWeight: "bold",
    cursor: loading ? "not-allowed" : "pointer",
    marginTop: "10px",
  };

  const resultBox = {
    marginTop: "20px",
    padding: "15px",
    background: "#1f2937",
    borderRadius: "8px",
  };

  const toggleButton = (active) => ({
    flex: 1,
    padding: "10px",
    background: active ? "#3b82f6" : "#374151",
    color: "white",
    border: "none",
    cursor: "pointer",
  });

  return (
    <div style={containerStyle}>
      <div style={cardStyle}>
        <h1 style={{ textAlign: "center", marginBottom: "20px" }}>
          🏀 NBA Simulator
        </h1>

        {/* Mode Toggle */}
        <div style={{ display: "flex", marginBottom: "15px" }}>
          <button
            onClick={() => setMode("game")}
            style={toggleButton(mode === "game")}
          >
            Game
          </button>

          <button
            onClick={() => setMode("season")}
            style={toggleButton(mode === "season")}
          >
            Season
          </button>
        </div>

        {/* Game Mode */}
        {mode === "game" ? (
          <>
            <input
              type="text"
              placeholder="Team 1"
              value={team1}
              onChange={(e) => setTeam1(e.target.value)}
              style={inputStyle}
            />

            <input
              type="text"
              placeholder="Team 2"
              value={team2}
              onChange={(e) => setTeam2(e.target.value)}
              style={inputStyle}
            />

            <button
              onClick={handleSimulate}
              style={buttonStyle}
              disabled={loading}
            >
              {loading ? "Simulating..." : "Simulate Game"}
            </button>
          </>
        ) : (
          <button
            onClick={handleSeasonSimulate}
            style={buttonStyle}
            disabled={loading}
          >
            {loading ? "Simulating Season..." : "Simulate Season"}
          </button>
        )}

        {/* Error */}
        {error && (
          <p style={{ color: "#f87171", marginTop: "10px" }}>{error}</p>
        )}

        {/* Game Result */}
        {result && mode === "game" && (
          <div style={resultBox}>
            <h2 style={{ marginBottom: "10px" }}>Result</h2>

            <p>
              <strong>Winner:</strong> {result.winner}
            </p>

            <p>
              <strong>{team1} Win Probability:</strong>{" "}
              {(result.team_a_win_probability * 100).toFixed(2)}%
            </p>

            <p>
              <strong>{team2} Win Probability:</strong>{" "}
              {(result.team_b_win_probability * 100).toFixed(2)}%
            </p>

            <p>
              <strong>Avg Score:</strong>{" "}
              {result.avg_score_a?.toFixed(1)} -{" "}
              {result.avg_score_b?.toFixed(1)}
            </p>
          </div>
        )}

        {/* Season Standings */}
        {Array.isArray(seasonData) &&
          seasonData.length > 0 &&
          mode === "season" && (
            <div style={resultBox}>
              <h2>Eastern Conference</h2>
              {east.map((team, i) => {
                const pct = (
                  team.wins /
                  (team.wins + team.losses)
                ).toFixed(3);

                return (
                  <p
                    key={i}
                    style={{
                      color:
                        i < 6
                          ? "#4ade80"
                          : i < 10
                          ? "#facc15"
                          : "white",
                    }}
                  >
                    {i + 1}. {team.team} — {team.wins}-{team.losses} ({pct})
                  </p>
                );
              })}

              <h2 style={{ marginTop: "15px" }}>
                Western Conference
              </h2>
              {west.map((team, i) => {
                const pct = (
                  team.wins /
                  (team.wins + team.losses)
                ).toFixed(3);

                return (
                  <p
                    key={i}
                    style={{
                      color:
                        i < 6
                          ? "#4ade80"
                          : i < 10
                          ? "#facc15"
                          : "white",
                    }}
                  >
                    {i + 1}. {team.team} — {team.wins}-{team.losses} ({pct})
                  </p>
                );
              })}
            </div>
          )}
      </div>
    </div>
  );
}

export default App;
