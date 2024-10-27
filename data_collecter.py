import requests
import concurrent.futures
from riotwatcher import LolWatcher, ApiError
from collections import defaultdict
from config import API_KEY

watcher = LolWatcher(API_KEY)

def get_summoner_puuid_by_riot_id(game_name, tag_line, region='americas'):
    """Get PUUID using Riot ID (game name and tag line)."""
    url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    headers = {"X-Riot-Token": API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()['puuid']
    except requests.exceptions.HTTPError as err:
        if response.status_code == 404:
            print("Riot ID not found.")
        elif response.status_code == 401:
            print("Unauthorized - check your API key.")
        else:
            print(f"HTTP error occurred: {err}")
    except requests.exceptions.RequestException as err:
        print(f"Request error: {err}")
    return None

def get_summoner_id_by_puuid(puuid, region='na1'):
    """Get summoner ID using PUUID."""
    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
    headers = {"X-Riot-Token": API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()['id']
    except requests.exceptions.HTTPError as err:
        if response.status_code == 404:
            print("PUUID not found.")
        elif response.status_code == 401:
            print("Unauthorized - check your API key.")
        else:
            print(f"HTTP error occurred: {err}")
    except requests.exceptions.RequestException as err:
        print(f"Request error: {err}")
    return None

def get_live_game_data(summoner_id, region='na1'):
    """Get current game information for a summoner."""
    url = f"https://{region}.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{summoner_id}"
    headers = {"X-Riot-Token": API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        if response.status_code == 404:
            print("Summoner is not currently in a game.")
        elif response.status_code == 401:
            print("Unauthorized - check your API key.")
        else:
            print(f"HTTP error occurred: {err}")
    except requests.exceptions.RequestException as err:
        print(f"Request error: {err}")
    return None

def get_champion_name_map():
    """Get a mapping of champion IDs to champion names using Data Dragon."""
    try:
        versions = requests.get('https://ddragon.leagueoflegends.com/api/versions.json').json()
        latest = versions[0]
        champions = requests.get(f'https://ddragon.leagueoflegends.com/cdn/{latest}/data/en_US/champion.json').json()
        
        champion_map = {}
        for champ_name, champ_data in champions['data'].items():
            champion_map[int(champ_data['key'])] = champ_name
            
        return champion_map
    except Exception as e:
        print(f"Error fetching champion data: {e}")
        return {}

def get_champion_specific_matches(region, puuid, champion_id, count=10):
    """Get and analyze matches for a specific champion."""
    try:
        matches = watcher.match.matchlist_by_puuid(region, puuid, count=100)  # Get more matches to filter
        champion_stats = {'wins': 0, 'games': 0, 'kills': 0, 'deaths': 0, 'assists': 0}
        matches_analyzed = 0
        
        # Use ThreadPoolExecutor for parallel match data retrieval
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_match = {
                executor.submit(watcher.match.by_id, region, match_id): match_id 
                for match_id in matches
            }
            
            for future in concurrent.futures.as_completed(future_to_match):
                if matches_analyzed >= count:  # Stop after analyzing desired number of matches
                    break
                    
                try:
                    match_data = future.result()
                    for participant in match_data['info']['participants']:
                        if participant['puuid'] == puuid and participant['championId'] == champion_id:
                            champion_stats['games'] += 1
                            champion_stats['wins'] += 1 if participant['win'] else 0
                            champion_stats['kills'] += participant['kills']
                            champion_stats['deaths'] += participant['deaths']
                            champion_stats['assists'] += participant['assists']
                            matches_analyzed += 1
                            break
                except Exception as e:
                    print(f"Error processing match: {e}")
                    continue
                    
        return champion_stats
    except ApiError as err:
        print(f"Failed to retrieve matches: {err}")
        return None

def get_champion_mastery(puuid, region='na1'):
    """Get top 5 champion mastery entries for a summoner using PUUID."""
    url = f"https://{region}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}"
    headers = {"X-Riot-Token": API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 403:
            print("Error: Champion mastery endpoint access is forbidden. Please check if your API key has the required permissions.")
            print("You may need to:\n1. Generate a new API key\n2. Ensure 'CHAMPION-MASTERY-V4' is enabled in your API key settings")
            return None
        response.raise_for_status()
        return response.json()[:5]  # Get top 5 champions
    except requests.exceptions.HTTPError as err:
        if response.status_code == 404:
            print(f"No mastery data found for PUUID: {puuid}")
        elif response.status_code == 401:
            print("Unauthorized - check your API key.")
        else:
            print(f"HTTP error occurred while fetching mastery data: {err}")
    except requests.exceptions.RequestException as err:
        print(f"Request error while fetching mastery data: {err}")
    return None

def get_champion_specific_matches_batch(region, puuid, count=100):
    """Get match history and process all champions at once."""
    try:
        # Get matches in one batch
        matches = watcher.match.matchlist_by_puuid(region, puuid, count=count)
        champion_stats = defaultdict(lambda: {'wins': 0, 'games': 0, 'kills': 0, 'deaths': 0, 'assists': 0})
        
        # Use ThreadPoolExecutor for parallel match data retrieval
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_match = {
                executor.submit(watcher.match.by_id, region, match_id): match_id 
                for match_id in matches
            }
            
            for future in concurrent.futures.as_completed(future_to_match):
                try:
                    match_data = future.result()
                    for participant in match_data['info']['participants']:
                        if participant['puuid'] == puuid:
                            champion_id = participant['championId']
                            stats = champion_stats[champion_id]
                            stats['games'] += 1
                            stats['wins'] += 1 if participant['win'] else 0
                            stats['kills'] += participant['kills']
                            stats['deaths'] += participant['deaths']
                            stats['assists'] += participant['assists']
                            break
                except Exception as e:
                    print(f"Error processing match: {e}")
                    continue
                    
        return champion_stats
    except ApiError as err:
        print(f"Failed to retrieve matches: {err}")
        return None

def get_champion_stats(game_name, tag_line, region='na1'):
    """Get champion mastery and win rates with optimized data retrieval."""
    print("Retrieving summoner information...")
    puuid = get_summoner_puuid_by_riot_id(game_name, tag_line)
    if not puuid:
        print("Error: Could not retrieve PUUID. Champion stats unavailable.")
        return None
        
    # Get champion mastery data
    print("Retrieving champion mastery data...")
    mastery_data = get_champion_mastery(puuid, region)
    if not mastery_data:
        print("Could not retrieve champion mastery data. Please check your API key permissions.")
        return None
    
    # Get champion name mapping
    champion_map = get_champion_name_map()
    champion_stats = []
    
    print("Analyzing match history for each champion...")
    # Process each champion's matches individually
    for champion in mastery_data:
        champion_id = champion['championId']
        print(f"Analyzing matches for {champion_map.get(champion_id, f'Champion {champion_id}')}...")
        
        # Get 10 matches for this specific champion
        match_stats = get_champion_specific_matches('americas', puuid, champion_id, count=10)
        
        if match_stats:
            win_rate = (match_stats['wins'] / match_stats['games'] * 100) if match_stats['games'] > 0 else 0
            kda = (match_stats['kills'] + match_stats['assists']) / max(1, match_stats['deaths']) if match_stats['games'] > 0 else 0
            
            champion_stats.append({
                'championId': champion_id,
                'championName': champion_map.get(champion_id, f"Champion {champion_id}"),
                'championLevel': champion['championLevel'],
                'championPoints': champion['championPoints'],
                'win_rate': win_rate,
                'games_analyzed': match_stats['games'],
                'kda': kda,
                'recent_performance': {
                    'kills_per_game': match_stats['kills'] / match_stats['games'] if match_stats['games'] > 0 else 0,
                    'deaths_per_game': match_stats['deaths'] / match_stats['games'] if match_stats['games'] > 0 else 0,
                    'assists_per_game': match_stats['assists'] / match_stats['games'] if match_stats['games'] > 0 else 0
                }
            })
    
    if not champion_stats:
        print("No champion statistics could be calculated.")
        return None
    
    # Sort by win rate in descending order
    champion_stats.sort(key=lambda x: x['win_rate'], reverse=True)
    return champion_stats

def get_match_history(region, puuid, count=10):
    """Get recent match history for a player."""
    try:
        matches = watcher.match.matchlist_by_puuid(region, puuid, count=count)
        match_details = []
        
        # Use ThreadPoolExecutor for parallel match data retrieval
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_match = {
                executor.submit(watcher.match.by_id, region, match_id): match_id 
                for match_id in matches
            }
            
            for future in concurrent.futures.as_completed(future_to_match):
                try:
                    match_data = future.result()
                    for participant in match_data['info']['participants']:
                        if participant['puuid'] == puuid:
                            match_details.append({
                                'win': participant['win'],
                                'duration': match_data['info']['gameDuration'],
                                'kills': participant['kills'],
                                'deaths': participant['deaths'],
                                'assists': participant['assists'],
                                'championId': participant['championId'],
                                'role': participant.get('teamPosition', 'Unknown'),
                                'vision_score': participant.get('visionScore', 0)
                            })
                            break
                except Exception as e:
                    print(f"Error processing match: {e}")
                    continue
                    
        return match_details
    except ApiError as err:
        print(f"Failed to retrieve match history: {err}")
        return None

def retrieve_match_data(game_name, tag_line, count):
    """Retrieve all match-related data for a player."""
    print(f"Requesting summoner data for '{game_name}#{tag_line}'")
    puuid = get_summoner_puuid_by_riot_id(game_name, tag_line)
    
    if not puuid:
        print("Failed to retrieve PUUID for summoner.")
        return None

    print(f"PUUID: {puuid}")

    summoner_id = get_summoner_id_by_puuid(puuid)
    
    if summoner_id:
        print(f"Summoner ID: {summoner_id}")
    else:
        print("Failed to retrieve summoner ID.")

    # Check if player is in game
    in_game_data = get_live_game_data(summoner_id)
    if in_game_data:
        print("Player is currently in-game!")
        
        for participant in in_game_data['participants']:
            riot_id = participant.get('riotId', 'Unknown')
            champion_id = participant['championId']
            print(f"{riot_id} - Champion ID: {champion_id}")
    else:
        print("Player is not in-game. Retrieving match history...")

    match_history = get_match_history("americas", puuid, count)
    return match_history

#Function to display champion_stats
def display_champion_stats(game_name, tag_line):
    """Display champion stats with improved formatting."""
    print("\nFetching champion mastery and win rate data...")
    stats = get_champion_stats(game_name, tag_line)
    
    if stats:
        print("\nTop 5 Mastery Champions (sorted by win rate):")
        print("-" * 100)
        print(f"{'Champion':<20} {'Level':<8} {'Mastery Points':<15} {'Win Rate':<12} {'Games':<8} {'KDA':<8}")
        print("-" * 100)
        
        for stat in stats:
            print(f"{stat['championName']:<20} "
                  f"{stat['championLevel']:<8} "
                  f"{stat['championPoints']:<15} "
                  f"{stat['win_rate']:.1f}%{' ':>6} "
                  f"{stat['games_analyzed']:<8} "
                  f"{stat['kda']:.2f}")