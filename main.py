from data_collecter import retrieve_match_data, get_champion_stats,display_champion_stats
from data_processing import save_data, load_data, calculate_metrics



    

def main():
    # Prompt for user inputs
    region = input("Enter the region (e.g., na1): ")
    game_name = input("Enter the summoner name: ")
    tag_line = input("Enter the tag line: ")

    while True:
        try:
            count = int(input("Enter the number of matches to retrieve: "))
            if count <= 0:
                print("Please enter a positive integer.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a number.")
            
    # Retrieve match data
    match_data = retrieve_match_data(game_name, tag_line, count)
    
    if match_data is None:
        print("No match data retrieved.")
        return
    
    # Save match data to CSV
    save_data(match_data, 'match_history.csv')
    print("Match data saved to match_history.csv")
    
    # Load and analyze match data
    loaded_data = load_data('match_history.csv')
    win_rate, average_duration = calculate_metrics(loaded_data)
    
    print(f"Win Rate: {win_rate:.2f}%")
    print(f"Average Game Duration: {average_duration} minutes")

    # Display champion stats
    print("\nRetrieving champion mastery and win rate data...")
    display_champion_stats(game_name, tag_line)

if __name__ == "__main__":
    main()