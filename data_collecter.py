import requests
from riotwatcher import LolWatcher, ApiError
from config import API_KEY
from champion_mapping import champion_mapping

watcher = LolWatcher(API_KEY)

def get_summoner_puuid_by_riot_id(game_name, tag_line, region='americas'):
    url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    headers = {"X-Riot-Token": API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
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
    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
    headers = {"X-Riot-Token": API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
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

def get_live_game_data(puuid, region='na1'):
    url = f"https://{region}.api.riotgames.com/lol/spectator/v5/active-games/by-summoner/{puuid}"
    headers = {"X-Riot-Token": API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()  # Return live game data
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

def get_match_history(region, puuid, count=10):
    try:
        match_history = watcher.match.matchlist_by_puuid(region, puuid, count=count)
        match_details = []
        for match_id in match_history:
            match_data = watcher.match.by_id(region, match_id)
            # Extract relevant details from the match data
            for participant in match_data['info']['participants']:
                if participant['puuid'] == puuid:  # Find the player in the match
                    match_details.append({
                        'win': participant['win'],
                        'duration': match_data['info']['gameDuration'],
                        'kills': participant['kills'],
                        'deaths': participant['deaths'],
                        'assists': participant['assists'],
                    })
        return match_details
    except ApiError as err:
        print(f"Failed to retrieve match history: {err}")
        return None

def retrieve_match_data(game_name, tag_line, count):
   
    print(f"Requesting summoner data for '{game_name}#{tag_line}'")
    puuid = get_summoner_puuid_by_riot_id(game_name, tag_line)
    
    if not puuid:
        print("Failed to retrieve PUUID for summoner.")
        return None

    # Print the PUUID
    print(f"PUUID: {puuid}")

    # Now retrieve the summoner ID using the PUUID
    summoner_id = get_summoner_id_by_puuid(puuid)
    
    # Print the summoner ID
    if summoner_id:
        print(f"Summoner ID: {summoner_id}")
    else:
        print("Failed to retrieve summoner ID.")

    # Check if the player is in-game
    in_game_data = get_live_game_data(puuid)
    if in_game_data:
        print("Player is currently in-game!")
        
    in_game_data = get_live_game_data(puuid)
    if in_game_data:
        print("Player is currently in-game!")

        for participant in in_game_data['participants']:
            riot_id = participant['riotId']
            champion_id = participant['championId']
            champion_name = champion_mapping.get(champion_id, "Unknown Champion")  # Get champion name

            print(f"{riot_id} - Champion: {champion_name}")

    else:
            print("Player is not in-game. Retrieving match history...")
        

    match_history = get_match_history("americas", puuid, count)
    return match_history
