import pandas as pd

def save_data(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)