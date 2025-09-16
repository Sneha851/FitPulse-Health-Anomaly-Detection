import pandas as pd

def load_data(file_path):
    """Load CSV file"""
    return pd.read_csv(file_path)

def preprocess_data(df, time_column, value_column):
    """Clean and prepare dataset"""
    df[time_column] = pd.to_datetime(df[time_column], errors='coerce')
    df = df.dropna()  # remove missing values
    df = df.sort_values(time_column)
    df = df.reset_index(drop=True)
    return df
