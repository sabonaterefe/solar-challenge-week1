import pandas as pd
import pytest
from app.utils import load_data

def test_load_data_multiple_files():
    # loading all countries clean datasets
    files = [
        "data/benin_clean.csv",
        "data/sierraleone_clean.csv",
        "data/togo_clean.csv"
    ]
    
    # Concatenating all data into a single DataFrame
    combined_data = pd.concat([load_data(file) for file in files], ignore_index=True)
    
    # testing if the combined DataFrame is a DataFrame
    assert isinstance(combined_data, pd.DataFrame)
    
    # testing if the DataFrame is not empty
    assert not combined_data.empty
    
    # updating expected columns based on  actual data structure
    expected_columns = {'GHI', 'DNI', 'DHI', 'ModA', 'ModB'}  # Adjust as necessary
    assert expected_columns.issubset(combined_data.columns)

def test_load_data_invalid_file():
    # testing loading an invalid CSV file
    with pytest.raises(FileNotFoundError):
        load_data("data/non_existent_file.csv")  