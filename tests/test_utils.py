import pandas as pd
import unittest
from app.utils import load_data

class TestUtils(unittest.TestCase):
    def test_load_data_multiple_files(self):
        """Test loading and combining multiple country datasets"""
        files = [
            "data/benin_clean.csv",
            "data/sierraleone_clean.csv",
            "data/togo_clean.csv"
        ]
    
        # Load and combine data
        combined_data = pd.concat(
            [load_data(file) for file in files],
            ignore_index=True
        )
        
        # Basic DataFrame checks
        self.assertIsInstance(combined_data, pd.DataFrame)
        self.assertFalse(combined_data.empty, "Combined DataFrame should not be empty")
        
        # Debug output for columns
        print("\n=== Actual Columns in Combined Data ===")
        print(combined_data.columns.tolist())
        
        # CORRECTED EXPECTED COLUMNS (matches your actual CSV headers)
        expected_columns = {
            'GHI', 
            'DNI', 
            'DHI', 
            'ModA',  # ✅ Matches actual column name
            'ModB'   # ✅ Matches actual column name
        }
        
        # Column validation
        missing_columns = expected_columns - set(combined_data.columns)
        self.assertEqual(
            len(missing_columns), 0,
            f"Missing expected columns: {missing_columns}"
        )
        
        # Additional validation
        self.assertGreaterEqual(
            len(combined_data), 1000,
            "Combined data should have significant entries"
        )

    def test_load_data_invalid_file(self):
        """Test handling of non-existent files"""
        with self.assertRaises(FileNotFoundError):
            load_data("data/non_existent_file.csv")

if __name__ == '__main__':
    unittest.main()