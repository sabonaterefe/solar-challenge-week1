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
    
        combined_data = pd.concat(
            [load_data(file) for file in files],
            ignore_index=True
        )
        
        self.assertIsInstance(combined_data, pd.DataFrame)
        self.assertFalse(combined_data.empty)
        
        print("\n=== Actual Columns in Combined Data ===")
        print(combined_data.columns.tolist())
        
        expected_columns = {'GHI', 'DNI', 'DHI', 'ModA', 'ModB'}
        missing_columns = expected_columns - set(combined_data.columns)
        self.assertEqual(len(missing_columns), 0, f"Missing columns: {missing_columns}")
        
        self.assertGreaterEqual(len(combined_data), 1000)
        
        for col in expected_columns:
            self.assertTrue(pd.api.types.is_numeric_dtype(combined_data[col]))
      
    def test_load_data_invalid_file(self):
        
        with self.assertRaises(FileNotFoundError):
            load_data("data/non_existent_file.csv")

if __name__ == '__main__':
    unittest.main()