#Project Jan Kardaszewicz 

#import libraries

import pandas as pd
import json
from pandas import DataFrame

import os
 
from geopy.geocoders import Nominatim
"""DATA PREPARATION"""

"""Getting geo data from files"""


def get_row_coordinates(row):
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

def get_row_price_for_m2(row):
    return round(row["Cena"] / row["Powierzchnia"], 2)

def prepare_data(data_str: str):
    df = pd.read_csv(data_str, sep=",")
    
    df["Cena"] = df["Cena"].str.replace(' ', '').astype(int)
    df["Powierzchnia"] = df["Powierzchnia"].str.replace(',', '.').astype(float)
    
    df["Cena_za_m2"] = df.apply(get_row_price_for_m2, axis=1)

    df["LatLong"] = df.apply(get_row_coordinates, axis=1)
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

def read_file(file_name: str):
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

MAIN_DF_path = read_file("inwestycje_data.csv")
ready_file_path = read_file("prepared_data.csv")
if not (os.path.exists(ready_file_path) and os.path.isfile(ready_file_path)):
    MAIN_DF = prepare_data(MAIN_DF_path)
    MAIN_DF.to_csv(ready_file_path, index=False)
else:
    MAIN_DF = pd.read_csv(ready_file_path)

with open(read_file("Dzielnice_administracyjne.geojson"),encoding="utf8") as f:
    MAIN_GJ = json.load(f)


"""Constants"""
CRACOW_CENTER = {"lat": 50.049683, "lon": 19.984544}
MAPBOX_STYLE = "carto-positron"
ZOOM = 10
districts = ["Stare Miasto","Grzegórzki", "Prądnik Czerwony", "Prądnik Biały", "Krowodrza", "Bronowice", "Zwierzyniec", "Dębniki", "Łagiewniki - Borek Fałęcki",
             "Swoszowice", "Podgórze Duchackie", "Bieżanów-Prokocim", "Podgórze", "Czyżyny", "Mistrzejowice", "Bieńczyce", "Wzgórza Krzesławickie", "Nowa Huta"]

PRICE_RANGE = 10000

MIN_PRICE_VALUE = int(MAIN_DF['Cena'].min()/PRICE_RANGE)*PRICE_RANGE
MAX_PRICE_VALUE = (int(MAIN_DF['Cena'].max()/PRICE_RANGE) + 1) * PRICE_RANGE

MIN_AREA_VALUE = int(MAIN_DF['Powierzchnia'].min())
MAX_AREA_VALUE = int(MAIN_DF['Powierzchnia'].max()) + 1 

"""Calculating the analysis data"""

def get_mean_price_data(data):
    dzielnice_srednia_cena = {"Dzielnica" : [], "srednia_cena": []}
    for dzielnica in set(data['Dzielnica']):
        df = data[data['Dzielnica'] == dzielnica]
        dzielnice_srednia_cena["Dzielnica"].append(dzielnica)
        dzielnice_srednia_cena["srednia_cena"].append(df["Cena"].mean())
    return pd.DataFrame(dzielnice_srednia_cena)

def get_mean_price_for_m2_data(data):
    dzielnice_srednia_cena = {"Dzielnica" : [], "srednia_cena_za_m2": []}
    for dzielnica in set(data['Dzielnica']):
        df = data[data['Dzielnica'] == dzielnica]
        dzielnice_srednia_cena["Dzielnica"].append(dzielnica)
        dzielnice_srednia_cena["srednia_cena_za_m2"].append(round(df["Cena_za_m2"].mean(),2))
    dzielnice_srednia_cena = pd.DataFrame(dzielnice_srednia_cena)
    dzielnice_srednia_cena = dzielnice_srednia_cena.sort_values(by="srednia_cena_za_m2")
    return dzielnice_srednia_cena

def get_mean_area_data(data):
    dzielnice_srednia_powierzchnia = {"Dzielnica" : [], "srednia_powierzchnia": []}
    for dzielnica in set(data['Dzielnica']):
        df = data[data['Dzielnica'] == dzielnica]
        dzielnice_srednia_powierzchnia["Dzielnica"].append(dzielnica)
        dzielnice_srednia_powierzchnia["srednia_powierzchnia"].append(round(df["Powierzchnia"].mean(),2))
    dzielnice_srednia_powierzchnia = pd.DataFrame(dzielnice_srednia_powierzchnia)
    dzielnice_srednia_powierzchnia = dzielnice_srednia_powierzchnia.sort_values(by='srednia_powierzchnia')
    return dzielnice_srednia_powierzchnia

mean_price_df_m2 = get_mean_price_for_m2_data(MAIN_DF)

mean_price_df = get_mean_price_data(MAIN_DF)

mean_area_df = get_mean_area_data(MAIN_DF)


def choose_df(df: DataFrame, dzielnice: list[str]):
    """
    Function choosing desired DataFrame.
    
    :param df: initial dataframe
    :type df: Dataframe
    :param dzielnice: chosen districts
    :type dzielnice: list[str]

    Returns:
        DataFrame: dataframe created according to chosen districts
    """
    new_df = df.loc[df["Dzielnica"].isin(dzielnice)]
    return new_df

def choose_gj(gj: dict, dzielnice: list[str]):
    """
    Function choosing desired Geojson.
    
    :param gj: initial Geojson file
    :type gj: geojson
    :param dzielnice: chosen districts

    Returns:
        dict: geojson created according to chosen districts
    """

    new_gj = {"type": "FeatureCollection",
    "name": "Dzielnice_administracyjne",
    "crs": {"type": "name",
    "properties": {"name": ""}},
    "features": []}

    for i in gj["features"]:
        if i["properties"]["nazwa"] in dzielnice:
            new_gj["features"].append(i)
    
    return new_gj

def choose_mean_df(df: DataFrame | list[DataFrame]):
    """
    Function calculating mean vaules of DataFrame parameters.

    :param df: DataFrame instance 

    Returns:
        touple(list[DataFrame],list[int]): touple of chosen DataFrame and found mean values.
    """
    res_graph = []
    res_data = []
    for df in df:
        ret_dict = {"Wartość": [df.columns[1]], "Aktualna średnia": [df.iloc[:, 1].mean()]}
        res_data.append(df.iloc[:, 1].mean())
        res_graph.append(pd.DataFrame(ret_dict))
    return res_graph, res_data

def set_df_price_and_area_range(df: DataFrame, price_range: list[float], area_range: list[float]):
    """Funciton choosing dispaly DataFrame according to sliders values.

        :param df: displayed DataFrame instance
        :type df: DataFrame
        :param price_range: price range-slider values
        :type price_range: list[float]
        :param area_range: area range-slider values
        :type area_range: list[float]
        
        Returns:
            DataFrame: chosen Datafreme with Price and Area values in sliders range.
    """
    df_range = df[(df['Cena'] >= price_range[0]) & (df['Cena'] <= price_range[1]) & (df['Powierzchnia'] >= area_range[0]) & (df['Powierzchnia'] <= area_range[1])]
    
    return df_range