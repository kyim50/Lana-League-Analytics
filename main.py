from data_collecter import retrieve_match_data
from data_processing import save_data

def main():
    region = "americas"
    summoner_name = input("Please enter your Summoner Name: ")
    match_data = retrieve_match_data(region, summoner_name)

    save_data(match_data, 'match_history.csv')

    print("Match data saved to match_history.csv")

if __name__ == "__main__":
    main()