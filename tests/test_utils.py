import pandas as pd
import unittest
from app.utils import load_data

class TestUtils(unittest.TestCase):  
    def test_load_data_multiple_files(self):
        files = [
            "data/benin_clean.csv",
            "data/sierraleone_clean.csv",
            "data/togo_clean.csv"
        ]
        combined_data = pd.concat([load_data(file) for file in files], ignore_index=True)
        
        self.assertIsInstance(combined_data, pd.DataFrame)
        self.assertFalse(combined_data.empty)
        
        expected_columns = {'GHI', 'DNI', 'DHI', 'ModA', 'ModB'}
        self.assertTrue(expected_columns.issubset(combined_data.columns))

    def test_load_data_invalid_file(self):
        with self.assertRaises(FileNotFoundError):  
            load_data("data/non_existent_file.csv")