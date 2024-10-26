from data_collecter import retrieve_match_data
from data_processing import save_data

def main():
    region = input("Enter the region (e.g., na1): ").strip()
    summoner_name = input("Enter the summoner name: ").strip()
    tag_line = input("Enter the tag line (e.g., '1234' from Riot ID): ").strip()

    match_data = retrieve_match_data(summoner_name, tag_line)

    if match_data:
        save_data(match_data, 'match_history.csv')
        print("Match data saved to match_history.csv")
    else:
        print("Failed to retrieve or save match data.")

if __name__ == "__main__":
    main()
