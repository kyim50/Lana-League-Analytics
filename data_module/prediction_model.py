import json
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from riotwatcher import LolWatcher
from config import API_KEY
from champion_mapping import champion_mapping  # Import the champion_mapping

watcher = LolWatcher(API_KEY)

# Load the match history data from a CSV file
df = pd.read_csv('match_history.csv')

# Function to map champion IDs to names
def map_champions(row):
    champ_id = row['championId']
    return champion_mapping.get(champ_id, "Unknown")

# Apply the mapping function to add a champion name column
df['championName'] = df.apply(map_champions, axis=1)

# Select relevant columns
df = df[['win', 'duration', 'kills', 'deaths', 'assists', 'championId', 'championName', 'role', 'vision_score']]

# Create dummy variables for roles
roles = ['TOP', 'JUNGLE', 'MID', 'BOTTOM', 'SUPPORT']
for role in roles:
    df[f'role_{role}'] = (df['role'] == role).astype(int)

# Drop the original role column
df.drop(columns=['role'], inplace=True)

# Show the updated DataFrame
print(df)

# Prepare data for model training
X = df.drop(columns=['win', 'championId', 'championName'])  # Features
y = df['win']  # Target variable

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Random Forest model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Make predictions
predictions = model.predict(X_test)

# Optionally, print predictions
print(predictions)
