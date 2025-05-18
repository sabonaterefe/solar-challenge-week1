import pandas as pd
import unittest
import os
from app.utils import load_data

class TestUtils(unittest.TestCase):
    def test_load_data_multiple_files(self):
        files = [
            "data/benin_clean.csv",
            "data/sierraleone_clean.csv",
            "data/togo_clean.csv"
        ]
        
        # Verify files exist
        for file in files:
            self.assertTrue(os.path.exists(file), f"File missing: {file}")

        # Load and combine data
        try:
            combined_data = pd.concat(
                [load_data(file) for file in files],
                ignore_index=True
            )
        except Exception as e:
            self.fail(f"Failed to load data: {e}")

        # Strip whitespace from column names
        combined_data.columns = combined_data.columns.str.strip()
        print(combined_data.head())

        self.assertIsInstance(combined_data, pd.DataFrame, "Combined data is not a DataFrame.")
        self.assertFalse(combined_data.empty, "Combined data is empty.")

        print("\n=== Actual Columns in Combined Data ===")
        print(combined_data.columns.tolist())

        expected_columns = {'GHI', 'DNI', 'DHI', 'ModA', 'ModB'}
        missing_columns = expected_columns - set(combined_data.columns)
        self.assertEqual(len(missing_columns), 0, f"Missing columns: {missing_columns}")

        self.assertGreaterEqual(len(combined_data), 1000, "Combined data has fewer than 1000 rows.")

        # **Fix Negative Values in Solar Data**
        for col in ['GHI', 'DNI', 'DHI']:
            combined_data[col] = combined_data[col].apply(lambda x: x if x >= 0 else None)

        # **Handle Missing Values (Updated for FutureWarning)**
        combined_data.ffill(inplace=True)  # Correct forward-fill approach

        # **Standardize Timestamp Formatting**
        combined_data['Timestamp'] = pd.to_datetime(combined_data['Timestamp'])

        # **Optimize Data Type Handling**
        numeric_columns = ['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'BP', 'TModA', 'TModB']
        combined_data[numeric_columns] = combined_data[numeric_columns].astype(float)

        # Ensure columns are numeric
        for col in expected_columns:
            self.assertIn(col, combined_data.columns, f"Expected column {col} is missing.")
            self.assertTrue(pd.api.types.is_numeric_dtype(combined_data[col]), f"Column {col} is not numeric.")

    def test_load_data_invalid_file(self):
        
        with self.assertRaises(FileNotFoundError):
            load_data("data/non_existent_file.csv")

if __name__ == '__main__':
    unittest.main()