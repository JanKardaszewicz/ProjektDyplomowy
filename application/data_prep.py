#Project Jan Kardaszewicz 

#import libraries

import pandas as pd
import json
from pandas import DataFrame
from abc import ABC
import os

from geopy.geocoders import Nominatim
"""DATA PREPARATION"""

"""Getting geo data from files"""

    
class Data(ABC):
    """
    Master Class to manage application shared data manipulation functionalities.
    """
    CRACOW_CENTER = {"lat": 50.049683, "lon": 19.984544}
    MAPBOX_STYLE = "carto-positron"
    ZOOM = 10
    districts = ["Stare Miasto","Grzegórzki", "Prądnik Czerwony", "Prądnik Biały", "Krowodrza", "Bronowice", "Zwierzyniec", "Dębniki", "Łagiewniki - Borek Fałęcki",
                    "Swoszowice", "Podgórze Duchackie", "Bieżanów-Prokocim", "Podgórze", "Czyżyny", "Mistrzejowice", "Bieńczyce", "Wzgórza Krzesławickie", "Nowa Huta"]
    PRICE_SCALING = 10000
    
    df_file = "inwestycje_data.csv"
    gj_file = "Dzielnice_administracyjne.geojson"
        

    def set_colors(self):
        """
        Function seting color for each district.
        
        Returns:
            dict: District : Color dictionary
        """
        COLORS = [
            "blue",
            "red", 
            "yellow", 
            "green",  
            "magenta",  
            "cyan",  
            "orange",
            "salmon", 
            "tan", 
            "lightblue",  
            "lightpink",  
            "teal",  
            "limegreen",  
            "gray",  
            "greenyellow",  
            "crimson", 
            "violet",  
            "sandybrown",
        ]   
        color_dict = {}  
        for i in range(len(self.districts)):
            color_dict[self.districts[i]] = COLORS[i]
            
        return color_dict

    def get_row_coordinates(self,row: dict):
        """
        Funciton returning coordinates by street name in Krakow.

        Args:
            row (dict): Data row

        Returns:
            list[flaot]: coordiantes
        """
        address = row["Ulica"] + " ,Kraków"
        geolocator = Nominatim(user_agent="geo_locator")

        try:
            location = geolocator.geocode(address)

            if location:
                    return location.latitude, location.longitude
            else:
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_row_price_for_m2(self, row: dict):
        """
        Function returning row price for m2.

        Args:
            row (dict): Data row

        Returns:
            float: price for m2 for row 
        """
        return round(row["Cena"] / row["Powierzchnia"], 2)

    def prepare_data(self, data_str: str):
        """
        Function preparing initial data for aplication.

        Args:
            data_str (str): data file name

        Returns:
            DataFrame: application data
        """
        df = pd.read_csv(data_str, sep=",")
        
        df["Cena"] = df["Cena"].str.replace(" ", "").astype(int)
        df["Powierzchnia"] = df["Powierzchnia"].str.replace(",", ".").astype(float)
        
        df["Cena_za_m2"] = df.apply(self.get_row_price_for_m2, axis=1)

        df["LatLong"] = df.apply(self.get_row_coordinates, axis=1)
        
        for index, row in df.iterrows():
            if row["LatLong"]:
                df.at[index, "lat"] = row["LatLong"][0]
                df.at[index, "lon"] = row["LatLong"][1]
            else:
                df.at[index, "lat"] = None
                df.at[index, "lon"] = None
        
        df = df.drop("LatLong", axis=1)
        df = df.dropna()
        return df

    def read_file(self, file_name: str):
        """Function to read files from data directory in Workspace.

        :param file_name: name of file to read
        :type file_name: str
        
        Returns:
            str: full file path
        """
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_directory = "../data"

        file_path = os.path.join(script_dir, data_directory, file_name)
        return file_path
    

class App_Data(Data):
    """Class to manage application main data"""
        
    def __init__(self) -> None:
        """
        Class init function to get inital DataFrame and Geojson structures.
        """
        self.DF_path = self.read_file(self.df_file)
        self.ready_file_path = self.read_file("prepared_data.csv")
        if not (os.path.exists(self.ready_file_path) and os.path.isfile(self.ready_file_path)):
            self.DF = self.prepare_data(self.DF_path)
            self.DF.to_csv(self.ready_file_path, index=False)
        else:
            self.DF = pd.read_csv(self.ready_file_path)

        with open(self.read_file(self.gj_file),encoding="utf8") as f:
            self.GJ = json.load(f)
    
    def return_df(self):
        """
        Function returning class DataFrame instance.

        Returns:
            DataFrame: class DataFrame instance
        """
        return self.DF
    
    def return_gj(self):
        """
        Function returning class Geojson instance.

        Returns:
            DataFrame: class Geojson instance
        """
        return self.GJ
      
    
    def return_districts(self):
        """
        Function returning class constant.

        Returns:
            list[str]: all districts of Krakow
        """
        return self.districts
    
    
    def return_MIN_PRICE_VALUE(self):
        """
        Function returning class constant.

        Returns:
            float: min value of class DF price column
        """
        MIN_PRICE_VALUE = int(self.DF["Cena"].min()/self.PRICE_SCALING)*self.PRICE_SCALING
        return MIN_PRICE_VALUE
    
    def return_MAX_PRICE_VALUE(self):
        """
        Function returning class constant.

        Returns:
            float: max value of class DF price column
        """
        MAX_PRICE_VALUE = (int(self.DF["Cena"].max()/self.PRICE_SCALING) + 1) * self.PRICE_SCALING
        return MAX_PRICE_VALUE
    
    def return_MIN_AREA_VALUE(self):
        """
        Function returning class constant.

        Returns:
            float: min value of class DF area column
        """
        MIN_AREA_VALUE = int(self.DF["Powierzchnia"].min())
        return MIN_AREA_VALUE
    
    def return_MAX_AREA_VALUE(self):
        """
        Function returning class constant.

        Returns:
            float: max value of class DF area column
        """
        MAX_AREA_VALUE = int(self.DF["Powierzchnia"].max()) + 1 
        return MAX_AREA_VALUE

    """Calculating the data"""

class Display_Data(App_Data):
    """
    Class to manage Display Layout type Data.
    """
    def __init__(self, price_range: list[float], area_range: list[float]) -> None:
        """
        Init function choosing DataFrame according to price_range and area_range.

        Args:
            price_range (list[float]): set price range for DataFrame
            area_range (list[float]): set area range for DataFrame
        """
        super().__init__()
        self.DF = self.set_df_price_and_area_range(price_range, area_range)
        
        
    def set_df_price_and_area_range(self, price_range: list[float], area_range: list[float]):
        """Funciton choosing dispaly DataFrame according to sliders values.

        :param price_range: price range-slider values
        :type price_range: list[float]
        :param area_range: area range-slider values
        :type area_range: list[float]
        
            Returns:
                DataFrame: chosen Datafreme with Price and Area values in sliders range.
        """
        df_range = self.DF[(self.DF["Cena"] >= price_range[0]) & (self.DF["Cena"] <= price_range[1]) & (self.DF["Powierzchnia"] >= area_range[0]) & (self.DF["Powierzchnia"] <= area_range[1])]
            
        return df_range              

    
class Analysis_Data(App_Data):
    """
    Class to manage Analysis layout type Data.

    Args:
        Data: Data class inheritence
    """
    def __init__(self, city_part: list[str]) -> None:
        """
        Init funciton to set mean DataFrame and modify initial DataFrame by city part.

        Args:
            city_part (list[str]): chosen city parts
        """
        super().__init__()
        self.city_part = city_part
        self.mean_df = self.set_means_DataFrame()
        self.DF = self.choose_df(self.DF)
        self.GJ = self.choose_gj()
        
    def return_mean_df(self):
        """
        Return Mean DataFrame instance.

        Returns:
            DataFrame: mean DataFrame 
        """
        return self.mean_df
    
    def set_means_DataFrame(self):
        """
        Function setting mean DataFrame instatnce - calculating mean area, price, price for m2 for DataFrame in Data object.

        Returns:
            DataFrame: mean DataFrame
        """
        dzielnice_srednia = {"Dzielnica" : [], "srednia_cena": [], "srednia_powierzchnia": [], "srednia_cena_za_m2": []}
        for dzielnica in set(self.DF["Dzielnica"]):
            df = self.DF[self.DF["Dzielnica"] == dzielnica]
            dzielnice_srednia["Dzielnica"].append(dzielnica)
            dzielnice_srednia["srednia_cena"].append(round(df["Cena"].mean(),2))
            dzielnice_srednia["srednia_cena_za_m2"].append(round(df["Cena_za_m2"].mean(),2))
            dzielnice_srednia["srednia_powierzchnia"].append(round(df["Powierzchnia"].mean(),2))
        return pd.DataFrame(dzielnice_srednia)
    
        
    def choose_df(self, df):
        """
        Function choosing desired DataFrame.
        
        :param df: DataFrame instance (could be mean_df or initial DF)
        :type df: Dataframe
        
        Returns:
            DataFrame: dataframe created according to chosen districts
        """
        new_df = df.loc[df["Dzielnica"].isin(self.city_part)]
        return new_df
    
    def choose_gj(self):
        """
        Function choosing desired Geojson.
        
        :param self.gj: initial Geojson file
        :type self.gj: geojson

        Returns:
            dict: geojson created according to chosen districts
        """

        new_gj = {"type": "FeatureCollection",
        "name": "Dzielnice_administracyjne",
        "crs": {"type": "name",
        "properties": {"name": ""}},
        "features": []}

        for i in self.GJ["features"]:
            if i["properties"]["nazwa"] in self.city_part:
                new_gj["features"].append(i)
        
        self.GJ = new_gj
        return new_gj
    
    def choose_mean_df(self, value: str):
        """
        Function calculating mean vaules of DataFrame parameters.

        :param value: which coulm of mean_df should be considered
        :type value: str
        
        Returns:
            touple(DataFrame, int): touple of chosen DataFrame and mean value.
        """
        df = self.choose_df(self.mean_df)
        res_data = df[value].mean()
        res_df = pd.DataFrame({"Wartość": value, "Aktualna średnia": [res_data]})
        return res_df, res_data
  
class Modify_Data(App_Data):
    """Class to maange modifying application data."""
    
    def __init__(self) -> None:
        """
        Function to initialize application data.
        """
        super().__init__()
        
    def add_data(self, Dzielnica: str, Ulica: str, Cena: float, Powierzchnia: float):
        """
        Function to add rows to DataFrame.

        Args:
            Dzielnica (str): added city part.
            Ulica (str): added street
            Cena (float): added price
            Powierzchnia (float): added area
            
        Returns:
            str: Inforation if data addition was successful
        """
        if Powierzchnia is None or Cena is None or Dzielnica is None or Ulica is None or Powierzchnia <= 0 or Cena <= 0 or len(Ulica) == 0 or len(Dzielnica) == 0 or Dzielnica not in self.districts:
            return "Zła wartość"
        added_row = {"Dzielnica": Dzielnica, "Ulica": Ulica, "Cena": Cena, "Powierzchnia": Powierzchnia}
        if not self.find_df_row(added_row):
            coordinates = self.get_row_coordinates(added_row)
            if coordinates is not None:
                added_row["lat"] = coordinates[0]
                added_row["lon"] = coordinates[1]
                added_row["Cena_za_m2"] = self.get_row_price_for_m2(added_row)
                self.DF.loc[len(self.DF)] = added_row
                self.DF.to_csv(self.ready_file_path)
                return f"Inwestycja dodana pomyślnie: {added_row}"
            else:
                return "Nie znaleziona współrzędnych podanego adresu!"
        else:
            return "Znaleziono istniejącą już taka inwestycje!"
        
    def find_df_row(self, added_row):
        """ 
        Check if any row in the DataFrame matches the added_row

        Args:
            added_row (dict): added row

        Returns:
            bool: infomation if row was found.
        """
        matching_rows = self.DF[
            (self.DF["Dzielnica"] == added_row["Dzielnica"]) &
            (self.DF["Ulica"] == added_row["Ulica"]) &
            (self.DF["Cena"] == added_row["Cena"]) &
            (self.DF["Powierzchnia"] == added_row["Powierzchnia"])
        ]
        return not matching_rows.empty