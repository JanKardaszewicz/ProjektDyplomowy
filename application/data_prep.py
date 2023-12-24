#Project Jan Kardaszewicz 

#import libraries

import pandas as pd
import json
from pandas import DataFrame

import os

from geopy.geocoders import Nominatim
"""DATA PREPARATION"""

"""Getting geo data from files"""

class Data_Prep:
    
    CRACOW_CENTER = {"lat": 50.049683, "lon": 19.984544}
    MAPBOX_STYLE = "carto-positron"
    ZOOM = 10
    districts = ["Stare Miasto","Grzegórzki", "Prądnik Czerwony", "Prądnik Biały", "Krowodrza", "Bronowice", "Zwierzyniec", "Dębniki", "Łagiewniki - Borek Fałęcki",
                    "Swoszowice", "Podgórze Duchackie", "Bieżanów-Prokocim", "Podgórze", "Czyżyny", "Mistrzejowice", "Bieńczyce", "Wzgórza Krzesławickie", "Nowa Huta"]
        
    
    def __init__(self) -> None:
        """Constants"""

        DF_path = self.read_file("inwestycje_data.csv")
        ready_file_path = self.read_file("prepared_data.csv")
        if not (os.path.exists(ready_file_path) and os.path.isfile(ready_file_path)):
            self.DF = self.prepare_data(DF_path)
            self.DF.to_csv(ready_file_path, index=False)
        else:
            self.DF = pd.read_csv(ready_file_path)

        with open(self.read_file("Dzielnice_administracyjne.geojson"),encoding="utf8") as f:
            self.GJ = json.load(f)
            
        PRICE_SCALING = 10000
        self.MIN_PRICE_VALUE = int(self.DF['Cena'].min()/PRICE_SCALING)*PRICE_SCALING
        self.MAX_PRICE_VALUE = (int(self.DF['Cena'].max()/PRICE_SCALING) + 1) * PRICE_SCALING

        self.MIN_AREA_VALUE = int(self.DF['Powierzchnia'].min())
        self.MAX_AREA_VALUE = int(self.DF['Powierzchnia'].max()) + 1 
    
    def return_df(self):
        return self.DF
    
    def return_gj(self):
        return self.GJ
    
    def return_districts(self):
        return self.districts
    
    def return_MIN_PRICE_VALUE(self):
        return self.MIN_PRICE_VALUE
    
    def return_MAX_PRICE_VALUE(self):
        return self.MAX_PRICE_VALUE
    
    def return_MIN_AREA_VALUE(self):
        return self.MIN_AREA_VALUE
    
    def return_MAX_AREA_VALUE(self):
        return self.MAX_AREA_VALUE
    
    def get_row_coordinates(self,row):
        address = row["Ulica"] + " ,Kraków"
        # Initialize the geolocator
        geolocator = Nominatim(user_agent="geo_locator")

        try:
            # Get location information from the address
            location = geolocator.geocode(address)

            if location:
                # Return the latitude and longitude
                    return location.latitude, location.longitude
            else:
                print("Location not found for the given address.")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_row_price_for_m2(self, row):
        return round(row["Cena"] / row["Powierzchnia"], 2)

    def prepare_data(self, data_str: str):
        df = pd.read_csv(data_str, sep=",")
        
        df["Cena"] = df["Cena"].str.replace(' ', '').astype(int)
        df["Powierzchnia"] = df["Powierzchnia"].str.replace(',', '.').astype(float)
        
        df["Cena_za_m2"] = df.apply(self.get_row_price_for_m2, axis=1)

        df["LatLong"] = df.apply(self.get_row_coordinates, axis=1)
        
        for index, row in df.iterrows():
            if row["LatLong"]:
                df.at[index, 'lat'] = row["LatLong"][0]
                df.at[index, 'lon'] = row["LatLong"][1]
            else:
                df.at[index, 'lat'] = None
                df.at[index, 'lon'] = None
        
        df = df.drop("LatLong", axis=1)
        df = df.dropna()
        return df

    def read_file(self, file_name: str):
        """Function to read files from data directory in Workspace

        :param file_name: name of file to read
        :type file_name: str
        
        Returns:
            str: full file path
        """
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_directory = "../data"

        file_name = file_name
        file_path = os.path.join(script_dir, data_directory, file_name)
        return file_path
    
    def set_colors(self):
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
    
    """Calculating the data"""
class Display_Data(Data_Prep):
    def __init__(self, price_range, area_range) -> None:
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
        df_range = self.DF[(self.DF['Cena'] >= price_range[0]) & (self.DF['Cena'] <= price_range[1]) & (self.DF['Powierzchnia'] >= area_range[0]) & (self.DF['Powierzchnia'] <= area_range[1])]
            
        return df_range              

    
class Analysis_Data(Data_Prep):
    def __init__(self) -> None:
        super().__init__()
        self.mean_df = self.set_means_DataFrame()
        
    def return_mean_df(self):
        return self.mean_df
    
    def set_means_DataFrame(self):
        dzielnice_srednia = {"Dzielnica" : [], "srednia_cena": [], "srednia_powierzchnia": [], "srednia_cena_za_m2": []}
        data = self.return_df()
        for dzielnica in set(data['Dzielnica']):
            df = data[data['Dzielnica'] == dzielnica]
            dzielnice_srednia["Dzielnica"].append(dzielnica)
            dzielnice_srednia["srednia_cena"].append(round(df["Cena"].mean(),2))
            dzielnice_srednia["srednia_cena_za_m2"].append(round(df["Cena_za_m2"].mean(),2))
            dzielnice_srednia["srednia_powierzchnia"].append(round(df["Powierzchnia"].mean(),2))
        return pd.DataFrame(dzielnice_srednia)
    
class Choose_Analysis_Data(Analysis_Data):
    
    def __init__(self, city_part) -> None:
        super().__init__() 
        self.city_part = city_part
        self.DF = self.choose_df(self.DF)
        self.GJ = self.choose_gj()
        self.mean_df = self.return_mean_df()
        
    def choose_df(self, df):
        """
        Function choosing desired DataFrame.
        
        :param df: initial dataframe
        :type df: Dataframe
        :param dzielnice: chosen districts
        :type dzielnice: list[str]

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
        :param self.city_part: chosen districts

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

        :param df: DataFrame instance 

        Returns:
            touple(list[DataFrame],list[int]): touple of chosen DataFrame and found mean values.
        """
        df = self.choose_df(self.mean_df)
        res_data = df[value].mean()
        res_df = pd.DataFrame({"Wartość": value, "Aktualna średnia": [res_data]})
        return res_df, res_data