from riotwatcher import LolWatcher
from config import API_KEY

watcher = LolWatcher (API_KEY)

def get_summoner_by_name(region, summoner_name):
    return watcher.summoner.by_name(region, summoner_name)

def get_match_history(match_region, summoner_puuid, count=10):
    return watcher.match.matchlist_by_puuid(match_region, summoner_puuid, count=count)

def retrieve_match_data(region, summoner_name):
    summoner_info = get_summoner_by_name(region, summoner_name)
    match_history = get_match_history("americas", summoner_info["puuid"])
    return match_history

def get_champion_data():
    versions = watcher.data_dragon.versions_for_regions("americas")
    latest_version = versions["n"]["champion"]
    champion_data = watcher.data_dragon.champions(latest_version, locale ="en_US")