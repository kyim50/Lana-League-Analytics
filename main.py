from data_collecter import retrieve_match_data
from data_processing import save_data, load_data, calculate_metrics
from visualization import plot_champion_performance, plot_win_rate
#from real_time_updater import display_game_state  # Import the real-time updater function

def main():
    # Prompt for user inputs
    region = input("Enter the region (e.g., na1): ")
    game_name = input("Enter the summoner name: ")
    tag_line = input("Enter the tag line: ")

    while True:
        try:
            count = int(input("Enter the number of matches you want to retrieve: "))
            if count > 0:  # Ensure the count is positive
                break
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # Retrieve match data
    match_data = retrieve_match_data(region, game_name, tag_line , count)
    
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
    print(f"Average Game Duration: {average_duration} seconds")

    # Optional: Call visualization functions if desired
    # plot_champion_performance(loaded_data)
    # plot_win_rate(loaded_data)

    # Start the real-time game updater
    print("\nStarting real-time game state updater...\n")
    #display_game_state(game_name, tag_line, region)  # This will keep running to update the game state

if __name__ == "__main__":
    main()
