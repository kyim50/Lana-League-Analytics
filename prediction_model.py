import pandas as pd


data = pd.read_csv("match_history.csv", index_col=0)
print(data)