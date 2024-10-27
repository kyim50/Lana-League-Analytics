from data_collecter import retrieve_match_data, get_champion_stats
from data_processing import save_data, load_data, calculate_metrics

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
    
    if stats:
        print("\nTop 5 Champions by Mastery (sorted by win rate):")
        print("-" * 70)
        print(f"{'Champion Level':<15} {'Mastery Points':<15} {'Win Rate':<15} {'Games Analyzed':<15}")
        print("-" * 70)
        
        for stat in stats:
            print(f"{stat['championLevel']:<15} {stat['championPoints']:<15} {stat['win_rate']:.1f}%{' ':>8} {stat['games_analyzed']:<15}")

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