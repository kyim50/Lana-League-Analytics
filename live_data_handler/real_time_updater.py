import requests
import urllib3

# Suppress the InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_live_client_data(endpoint):
    url = f"https://127.0.0.1:2999/liveclientdata/{endpoint}"
    try:
        response = requests.get(url, verify=False)  # Disable verification for local requests
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()  # Return JSON data if successful
    except requests.exceptions.RequestException as e:
        print(f"HTTP error occurred: {e}")
        return None  # Return None if there was an error

def get_players_data():
    # Fetch the player data
    players_data = get_live_client_data("activeplayer")
    if players_data:
        return players_data  # Return data for the current player

    # If active player data isn't found, attempt to get player data by riot ID
    players = get_live_client_data("allplayers")
    if players:
        return players  # Return all player data if available
    return None

def display_player_data(player):
    print("Player Data Structure:", player)  # Debugging output to check the player data structure

    # Display comprehensive player information
    try:
        print(f"Player: {player['summonerName']}")
        print(f"Riot ID: {player['riotId']}")
        print(f"Champion: {player.get('abilities', {}).get('Q', {}).get('displayName', 'N/A')}")
        print(f"Level: {player['level']}")
        print(f"Current Gold: {player['currentGold']}")
        print(f"Health: {player['championStats']['currentHealth']}/{player['championStats']['maxHealth']}")
        print(f"Attack Damage: {player['championStats']['attackDamage']}")
        print(f"Armor: {player['championStats']['armor']}")
        print(f"Magic Resist: {player['championStats']['magicResist']}")
        print(f"Movement Speed: {player['championStats']['moveSpeed']}")
        print(f"Abilities: {[ability['displayName'] for ability in player['abilities'].values()]}")
        print(f"Runes: {[rune['displayName'] for rune in player['fullRunes']['generalRunes']]}")
        
        # Fetch items safely
        items_data = get_live_client_data(f'playeritems?riotId={player["riotId"]}')
        if items_data:
            print(f"Items: {[item['displayName'] for item in items_data]}")
        else:
            print("Items data not available.")

        print("----------")
    except KeyError as e:
        print(f"KeyError: {e} - Player data may be missing some fields.")

def main():
    players_data = get_players_data()

    if players_data:
        if isinstance(players_data, list):
            for player in players_data:
                display_player_data(player)
        else:
            display_player_data(players_data)
    else:
        print("Failed to retrieve player data.")

if __name__ == "__main__":
    main()
