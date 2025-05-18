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

        for file in files:
            self.assertTrue(os.path.exists(file), f"File missing: {file}")

        try:
            combined_data = pd.concat(
                [load_data(file) for file in files],
                ignore_index=True
            )
        except Exception as e:
            self.fail(f"Failed to load data: {e}")

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

        for col in ['GHI', 'DNI', 'DHI']:
            combined_data[col] = combined_data[col].apply(lambda x: x if x >= 0 else None)

        combined_data.ffill(inplace=True)
        combined_data['Timestamp'] = pd.to_datetime(combined_data['Timestamp'])

        numeric_columns = ['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'BP', 'TModA', 'TModB']
        combined_data[numeric_columns] = combined_data[numeric_columns].astype(float)

        for col in expected_columns:
            self.assertIn(col, combined_data.columns, f"Expected column {col} is missing.")
            self.assertTrue(pd.api.types.is_numeric_dtype(combined_data[col]), f"Column {col} is not numeric.")

    def test_load_data_invalid_file(self):
        with self.assertRaises(FileNotFoundError):
            load_data("data/non_existent_file.csv")

    def test_load_data_empty_file(self):
        empty_file = "data/empty_file.csv"
        pd.DataFrame().to_csv(empty_file, index=False)

        with self.assertRaises(ValueError):
            load_data(empty_file)

        os.remove(empty_file)

    def test_numeric_columns(self):
        files = [
            "data/benin_clean.csv",
            "data/sierraleone_clean.csv",
            "data/togo_clean.csv"
        ]

        combined_data = pd.concat(
            [load_data(file) for file in files],
            ignore_index=True
        )

        numeric_columns = ['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'BP', 'TModA', 'TModB']
        for col in numeric_columns:
            self.assertIn(col, combined_data.columns, f"Column {col} is missing.")
            self.assertTrue(pd.api.types.is_numeric_dtype(combined_data[col]), f"Column {col} is not numeric.")

if __name__ == '__main__':
    unittest.main()