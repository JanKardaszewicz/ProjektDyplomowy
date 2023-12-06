#Project Jan Kardaszewicz 

#import libraries

import pandas as pd
import json
from pandas import DataFrame

import os 
"""DATA PREPARATION"""

"""Constants"""
CRACOW_CENTER = {"lat": 50.049683, "lon": 19.984544}
MAPBOX_STYLE = "carto-positron"
ZOOM = 10
districts = ["Stare Miasto","Grzegórzki", "Prądnik Czerwony", "Prądnik Biały", "Krowodrza", "Bronowice", "Zwierzyniec", "Dębniki", "Łagiewniki-Borek Fałęcki",
             "Swoszowice", "Podgórze Duchackie", "Bieżanów-Prokocim", "Podgórze", "Czyżyny", "Mistrzejowice", "Bieńczyce", "Wzgórza Krzesławickie", "Nowa Huta"]

"""Getting geo data from files"""
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

#TODO Automat do pozyskania wiekszej liczby danych lub jakos pozyskac duzo danych nwm jak jeszcze :(
df = pd.read_csv(read_file("mieszkania.csv") , sep=";")
with open(read_file("Dzielnice_administracyjne2.geojson"),encoding="utf8") as f:
    gj = json.load(f)

#TODO Narazie uzywam gotowych plikow utworzonych losowo - wyliaczanie srednich dopiero po uzyskaniu wiekszej liczby dancyh

"""Calculating the analysys data"""

mean_price_df = pd.read_csv(read_file("mieszkania_srednia.csv"))
mean_price_df["srednia_cena_za_m2"] = pd.to_numeric(mean_price_df["srednia_cena_za_m2"])

mean_area_df = pd.read_csv(read_file("mieszkania_powierzchnia.csv"))
mean_area_df["srednia_powierzchnia"] = pd.to_numeric(mean_area_df["srednia_powierzchnia"])


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
    """Function calculating mean vaules of DataFrame parameters.

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