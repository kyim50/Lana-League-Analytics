import numpy as np
from riotwatcher import LolWatcher
from config import API_KEY

watcher = LolWatcher(API_KEY)


def get_live_match_data(region, summoner_id):
    try:
        match_data = watcher.spectator.by_summoner(region, summoner_id)
        
        # Extract participants
        team_composition = match_data['participants']
        current_game_state = {
            "gold_lead": match_data['gold_lead'],
            "kills": sum(player['kills'] for player in team_composition),
            "deaths": sum(player['deaths'] for player in team_composition),
            "assists": sum(player['assists'] for player in team_composition),
            "objectives": {
                "towers": sum(player['tower_kills'] for player in team_composition),
                "dragons": sum(player['dragon_kills'] for player in team_composition),
                "barons": sum(player['baron_kills'] for player in team_composition),
            },
            "cs": sum(player['cs'] for player in team_composition),
            "avg_level": np.mean([player['champion_level'] for player in team_composition]),
            "vision_score": sum(player['vision_score'] for player in team_composition),
        }
        return team_composition, current_game_state
    except Exception as e:
        print(f"Error fetching match data: {e}")
        return None, None

def calculate_win_probability(team_composition, current_game_state):
    base_probability = 0.5
    
    # Factors contributing to win probability
    if current_game_state["gold_lead"] > 2000:
        base_probability += 0.1
    if current_game_state["kills"] > current_game_state["deaths"]:
        base_probability += 0.05  # Positive KDA
    if current_game_state["objectives"]["dragons"] > 1:
        base_probability += 0.05  # Objective advantage
    if current_game_state["vision_score"] > 30:
        base_probability += 0.05  # Vision control

    # Normalize to ensure probability remains between 0 and 1
    return min(max(base_probability, 0), 1)

