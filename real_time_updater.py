from riotwatcher import LolWatcher
from config import API_KEY

watcher = LolWatcher(API_KEY)

def get_live_match_data(region, summoner_id):
    try:
        return watcher.spectator.by_summoner(region, summoner_id)
    except:
        return None
    
def calculate_win_probability(team_composition, current_game_state):
    base_probability = 0.5
    if current_game_state["gold_lead"] > 3000:
        base_probability += 0.1
    return base_probability