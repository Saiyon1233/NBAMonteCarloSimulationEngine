# NBA Monte Carlo Simulation Engine

## Overview
This project is an NBA game simulation engine powered by a Monte Carlo approach. It uses team offensive and defensive ratings from the NBA API to simulate games thousands of times and estimate win probabilities and expected scores. A React frontend allows users to input two teams and view simulation results in real time.

## Features
- Fetches real-time NBA team statistics using nba_api
- Computes expected scores using offensive and defensive ratings
- Runs Monte Carlo simulations to estimate win probabilities
- Predicts game outcomes with average score projections
- Interactive React frontend for user input and results display

## Project Structure
- `server.py`: Flask API endpoint that handles simulation requests
- `model.py`: Fetches NBA team data and computes expected scores
- `simulation.py`: Runs Monte Carlo simulations
- `game.py`: Simulates a single game using probabilistic scoring
- `App.js`: React frontend UI for user input and displaying results
- `requirements.txt`: Python backend dependencies

## Setup
1. Clone the repository to your local machine:  
   git clone <repo-url>

2. Navigate to the project directory:  
   nbaMonteCarloSimulationEngine

3. Install backend dependencies:  
   pip install flask flask-cors pandas numpy nba_api

4. Run the backend server:  
   cd backend  
   python server.py

5. Run the frontend application:  
   cd frontend  
   npm install  
   npm start

6. Open the app in your browser at:  
   http://localhost:3000

## Skills, Technologies and Tools Used
- Python
- Flask
- React
- Axios
- NumPy
- Pandas
- nba_api
- Monte Carlo Simulation