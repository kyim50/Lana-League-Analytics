import matplotlib.pyplot as plt
import seaborn as sns

def plot_champion_performance(data):
    """Plot the performance of champions."""
    plt.figure(figsize=(10, 6))
    sns.barplot(data=data, x='champion', y='kda', palette='viridis')
    plt.title('Champion Performance: KDA')
    plt.xlabel('Champion')
    plt.ylabel('KDA')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_win_rate(data):
    """Plot the win rate of champions."""
    plt.figure(figsize=(10, 6))
    sns.barplot(data=data, x='champion', y='win_rate', palette='magma')
    plt.title('Champion Win Rates')
    plt.xlabel('Champion')
    plt.ylabel('Win Rate (%)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
