import pandas as pd

def load_data(file_path):
    """Load CSV data from the specified file path."""
    return pd.read_csv(file_path)