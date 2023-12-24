import unittest
import pandas as pd
from data_prep import *

class TestDataPrep(unittest.TestCase):

    def setUp(self):
        self.data_prep = Data_Prep()

    def test_return_df(self):
        self.assertIsInstance(self.data_prep.return_df(), pd.DataFrame)

    def test_return_gj(self):
        self.assertIsInstance(self.data_prep.return_gj(), dict)

    def test_return_districts(self):
        self.assertIsInstance(self.data_prep.return_districts(), list)

    def test_return_MIN_PRICE_VALUE(self):
        self.assertIsInstance(self.data_prep.return_MIN_PRICE_VALUE(), int)

    def test_return_MAX_PRICE_VALUE(self):
        self.assertIsInstance(self.data_prep.return_MAX_PRICE_VALUE(), int)

    def test_return_MIN_AREA_VALUE(self):
        self.assertIsInstance(self.data_prep.return_MIN_AREA_VALUE(), int)

    def test_return_MAX_AREA_VALUE(self):
        self.assertIsInstance(self.data_prep.return_MAX_AREA_VALUE(), int)

    def test_get_row_coordinates(self):
        # Assuming a row with a valid address
        row = {"Ulica": "Świętego Sebastiana"}
        self.assertIsNotNone(self.data_prep.get_row_coordinates(row))

    def test_get_row_price_for_m2(self):
        # Assuming a row with valid 'Cena' and 'Powierzchnia'
        row = {"Cena": 100000, "Powierzchnia": 50}
        result = self.data_prep.get_row_price_for_m2(row)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 2000)



class TestDisplayData(unittest.TestCase):

    def setUp(self):
        self.display_data = Display_Data(price_range=[0, 1000000], area_range=[0, 200])

    def test_set_df_price_and_area_range(self):
        self.assertIsInstance(self.display_data.set_df_price_and_area_range([0, 1000000], [0, 200]), pd.DataFrame)


class TestAnalysisData(unittest.TestCase):

    def setUp(self):
        self.analysis_data = Analysis_Data()

    def test_return_mean_df(self):
        self.assertIsInstance(self.analysis_data.return_mean_df(), pd.DataFrame)

    def test_set_means_DataFrame(self):
        self.assertIsInstance(self.analysis_data.set_means_DataFrame(), pd.DataFrame)


class TestChooseAnalysisData(unittest.TestCase):

    def setUp(self):
        self.choose_analysis_data = Choose_Analysis_Data(city_part=["Stare Miasto", "Grzegórzki"])

    def test_choose_df(self):
        df = pd.DataFrame({"Dzielnica": ["Stare Miasto", "Grzegórzki"], "Cena": [100000, 200000]})
        res = self.choose_analysis_data.choose_df(df)
        self.assertIsInstance(res, pd.DataFrame)
        self.assertEqual(res["Dzielnica"][0], df["Dzielnica"][0])
        self.assertEqual(res["Cena"][0], df["Cena"][0])

    def test_choose_gj(self):
        self.assertIsInstance(self.choose_analysis_data.choose_gj(), dict)
        self.assertGreater(len(self.choose_analysis_data.choose_gj()), 0)

    def test_choose_mean_df(self):
        res = self.choose_analysis_data.choose_mean_df("srednia_cena")
        self.assertIsInstance(res, tuple)
        self.assertTrue(float(res[0]["Aktualna średnia"].iloc[0]) == res[1])


if __name__ == '__main__':
    unittest.main()
