import unittest
import pandas as pd

# Assume that the code is saved in a file named "your_code.py"

# Import the code for testing
from data import choose_df, choose_gj, choose_mean_df

class TestYourCode(unittest.TestCase):
    def test_choose_df(self):
        # Test chooseing df 
        df = pd.DataFrame({"Dzielnica": ["A", "B", "C", "D"],
                       "Value": [1, 2, 3, 4]})
        dzielnice = ["A", "C"]
        result_df = choose_df(df, dzielnice)
        expected_df = pd.DataFrame({"Dzielnica": ["A", "C"],
                                    "Value": [1, 3]}).reset_index(drop=True)
        pd.testing.assert_frame_equal(result_df.reset_index(drop=True), expected_df)
    
    def test_choose_gj(self):
        # Test choose_gj function
        gj = {
            "type": "FeatureCollection",
            "features": [
                {"properties": {"nazwa": "A"}},
                {"properties": {"nazwa": "B"}},
                {"properties": {"nazwa": "C"}},
                {"properties": {"nazwa": "D"}}
            ]
        }
        dzielnice = ["A", "C"]
        result_gj = choose_gj(gj, dzielnice)
        expected_gj = {
            "type": "FeatureCollection",
            'name': 'Dzielnice_administracyjne', 
            'crs': {'type': 'name', 'properties': {'name': ''}},
            "features": [
                {"properties": {"nazwa": "A"}},
                {"properties": {"nazwa": "C"}}
            ]
        }
        self.assertDictEqual(result_gj, expected_gj)

    def test_choose_mean_df(self):
        # Test choose_mean_df function
        df1 = pd.DataFrame({"Dzielnica": ["Stare Miasto", "Grzegórzki", "Kazimierz"],
                            "średnia cena za m2": [1, 2, 3]})
        df2 = pd.DataFrame({"Dzielnica": ["Stare Miasto", "Grzegórzki", "Kazimierz"],
                            "średnia powierzchnia": [4, 5, 6]})
        result_df, result_data = choose_mean_df([df1, df2])
        print(result_df[0])
        expected_df = [pd.DataFrame({"Wartość": ["średnia cena za m2"], "Aktualna średnia": [2.0]}),
                          pd.DataFrame({"Wartość": ["średnia powierzchnia"], "Aktualna średnia": [5.0]})]
        expected_data = [2.0, 5.0]
        for res, exp in zip(result_df, expected_df):
            pd.testing.assert_frame_equal(res, exp)
        self.assertEqual(result_data, expected_data)

if __name__ == '__main__':
    unittest.main()
