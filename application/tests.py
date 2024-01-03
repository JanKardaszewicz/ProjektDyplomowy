import unittest
import pandas as pd
from data_prep import *

class TestDataPrep(unittest.TestCase):
    
    def setUp(self):
        self.data_prep = Data()

    def test_get_row_coordinates(self):
        # Assuming a row with a valid address
        row = {"Ulica": "Świętego Sebastiana"}
        self.assertIsNotNone(self.data_prep.get_row_coordinates(row))

    def test_get_row_price_for_m2(self):
        # Assuming a row with valid "Cena" and "Powierzchnia"
        row = {"Cena": 100000, "Powierzchnia": 50}
        result = self.data_prep.get_row_price_for_m2(row)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 2000)

class TestData(unittest.TestCase):
    
    def setUp(self):
        self.test_data = App_Data()
    
    def test_return_df(self):
        self.assertIsInstance(self.test_data.return_df(), pd.DataFrame)

    def test_return_gj(self):
        self.assertIsInstance(self.test_data.return_gj(), dict)

    def test_return_districts(self):
        self.assertIsInstance(self.test_data.return_districts(), list)

    def test_return_MIN_PRICE_VALUE(self):
        self.assertIsInstance(self.test_data.return_MIN_PRICE_VALUE(), int)

    def test_return_MAX_PRICE_VALUE(self):
        self.assertIsInstance(self.test_data.return_MAX_PRICE_VALUE(), int)

    def test_return_MIN_AREA_VALUE(self):
        self.assertIsInstance(self.test_data.return_MIN_AREA_VALUE(), int)

    def test_return_MAX_AREA_VALUE(self):
        self.assertIsInstance(self.test_data.return_MAX_AREA_VALUE(), int)
    
class TestDisplayData(unittest.TestCase):

    def setUp(self):
        self.display_data = Display_Data(price_range=[0, 1000000], area_range=[0, 200])

    def test_set_df_price_and_area_range(self):
        df = pd.DataFrame({"Dzielnica": ["A", "B", "C", "D"],
                    "Powierzchnia": [1, 2, 3, 4],
                    "Cena": [100, 200, 300, 400]})
        
        result_df = self.display_data.set_df_price_and_area_range(df, [150, 350], [3, 4])
        self.assertIsInstance(result_df , pd.DataFrame)
        
        expected_df = pd.DataFrame({"Dzielnica": ["C"],
                                    "Powierzchnia": [3],
                                    "Cena": [300]}).reset_index(drop=True)
        
        pd.testing.assert_frame_equal(result_df.reset_index(drop=True), expected_df)


class TestAnalysisData(unittest.TestCase):

    def setUp(self):
        self.analysis_data = Analysis_Data(city_part=["Stare Miasto", "Grzegórzki"])

    def test_return_mean_df(self):
        self.assertIsInstance(self.analysis_data.return_mean_df(), pd.DataFrame)

    def test_return_mean_area(self):
        self.assertIsInstance(self.analysis_data.return_mean_area(), dict)
        
    def test_choose_df(self):
        df = pd.DataFrame({"Dzielnica": ["A", "B", "C", "D"],
                    "Value": [1, 2, 3, 4]})
        city_part = ["A", "C"]
        result_df = self.analysis_data.choose_df(df, city_part)
        expected_df = pd.DataFrame({"Dzielnica": ["A", "C"],
                                    "Value": [1, 3]}).reset_index(drop=True)
        pd.testing.assert_frame_equal(result_df.reset_index(drop=True), expected_df)
    
    def test_choose_gj(self):
        gj = {
            "type": "FeatureCollection",
            "features": [
                {"properties": {"nazwa": "A"}},
                {"properties": {"nazwa": "B"}},
                {"properties": {"nazwa": "C"}},
                {"properties": {"nazwa": "D"}}
            ]
        }
        city_part = ["A", "C"]
        result_gj = self.analysis_data.choose_gj(gj, city_part)
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
        res = self.analysis_data.choose_mean_df("srednia_cena", city_part=["Stare Miasto", "Grzegórzki"])
        self.assertIsInstance(res, dict)
        self.assertTrue(float(res["df"]["Aktualna średnia"].iloc[0]) == res["value"])

class Test_Modify_Data(unittest.TestCase):
    def setUp(self):
        self.test_data = Modify_Data()
    
    def test_find_row_non_existent(self):
        df_row = {"Dzielnica": "S", "Ulica": "S", "Cena" : 1, "Powierzchnia":1}
        res = self.test_data.find_df_row(df_row)
        self.assertEqual(res, False)
        
    def test_find_row_exists(self):
        df_row = {"Dzielnica": "Stare Miasto", "Ulica": "Świętego Sebastiana 18", "Cena" : 631375, "Powierzchnia": 24.5}
        res = self.test_data.find_df_row(df_row)
        self.assertEqual(res, True)
        
    def test_add_data_wrong_value(self):
        result = self.test_data.add_data("wrong_dzielnica", "al. 29 Listopada", 400.0, 80.0)
        self.assertEqual(result, "Zła wartość")
        result = self.test_data.add_data("Stare Miasto","al. 29 Listopada", 400, -8 )
        self.assertEqual(result, "Zła wartość")
        result = self.test_data.add_data("Stare Miasto","al. 29 Listopada", 0, 8 )
        self.assertEqual(result, "Zła wartość")
        
    def test_add_data_missing_coordinates(self):
        # Test adding an investment with missing coordinates
        result = self.test_data.add_data("Stare Miasto", "NonexistentStreet", 400.0, 80.0)
        self.assertEqual(result, "Nie znaleziono współrzędnych podanego adresu!")
    
    def test_add_data_row_exists(self):
        result = self.test_data.add_data("Stare Miasto", "Świętego Sebastiana 18", 631375, 24.5)
        self.assertEqual(result, "Inwestycja już istnieje w bazie!")


if __name__ == "__main__":
    unittest.main()
