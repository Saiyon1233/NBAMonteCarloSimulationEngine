import React, { useState } from "react";
import axios from "axios";

function App() {
  const [team1, setTeam1] = useState("");
  const [team2, setTeam2] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

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

  return (
    <div style={containerStyle}>
      <div style={cardStyle}>
        <h1 style={{ textAlign: "center", marginBottom: "20px" }}>
          🏀 NBA Simulator
        </h1>

        <input
          type="text"
          placeholder="Team 1 (e.g. Los Angeles Lakers)"
          value={team1}
          onChange={(e) => setTeam1(e.target.value)}
          style={inputStyle}
        />

        <input
          type="text"
          placeholder="Team 2 (e.g. Boston Celtics)"
          value={team2}
          onChange={(e) => setTeam2(e.target.value)}
          style={inputStyle}
        />

        <button onClick={handleSimulate} style={buttonStyle} disabled={loading}>
          {loading ? "Simulating..." : "Simulate Game"}
        </button>

        {error && (
          <p style={{ color: "#f87171", marginTop: "10px" }}>{error}</p>
        )}

        {result && (
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
      </div>
    </div>
  );
}

export default App;