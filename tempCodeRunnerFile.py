
    # Load and analyze match data
    loaded_data = load_data('match_history.csv')
    win_rate, average_duration = calculate_metrics(loaded_data)
    
    print(f"Win Rate: {win_rate:.2f}%")
    print(f"Average Game Duration: {average_duration/60} minutes")

    # Optional: Call visualization functions if desired
    # plot_champion_performance(loaded_data)
    # plot_win_rate(loaded_data)
