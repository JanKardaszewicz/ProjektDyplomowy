#Project Jan Kardaszewicz 

#import libraries

import pandas as pd
import json
from pandas import DataFrame

"""DATA PREPARATION"""

"""Constants"""
CRACOW_CENTER = {"lat": 50.049683, "lon": 19.984544}
MAPBOX_STYLE = "carto-positron"
ZOOM = 10
districts = ["Stare Miasto","Grzegórzki", "Prądnik Czerwony", "Prądnik Biały", "Krowodrza", "Bronowice", "Zwierzyniec", "Dębniki", "Łagiewniki-Borek Fałęcki",
             "Swoszowice", "Podgórze Duchackie", "Bieżanów-Prokocim", "Podgórze", "Czyżyny", "Mistrzejowice", "Bieńczyce", "Wzgórza Krzesławickie", "Nowa Huta"]

"""Getting geo data from files"""

#TODO Automat do pozyskania wiekszej liczby danych lub jakos pozyskac duzo danych nwm jak jeszcze :(
df = pd.read_csv("mieszkania.csv", sep=";")
with open("Dzielnice_administracyjne2.geojson",encoding="utf8") as f:
    gj = json.load(f)

#TODO Narazie uzywam gotowych plikow utworzonych losowo - wyliaczanie srednich dopiero po uzyskaniu wiekszej liczby dancyh

"""Calculating the analysys data"""

mean_price_df = pd.read_csv("mieszkania_srednia.csv")
mean_price_df["srednia_cena_za_m2"] = pd.to_numeric(mean_price_df["srednia_cena_za_m2"])

mean_area_df = pd.read_csv("mieszkania_powierzchnia.csv")
mean_area_df["srednia_powierzchnia"] = pd.to_numeric(mean_area_df["srednia_powierzchnia"])


def choose_df(df: DataFrame, dzielnice: list[str]) -> DataFrame:
    """
    Function choosing desired DataFrame.
    
    :param df: initial dataframe
    :param dzielnice: chosen districts
    :return: dataframe created according to chosen districts
    """
    new_df = df.loc[df["Dzielnica"].isin(dzielnice)]
    return new_df

def choose_gj(gj: dict, dzielnice: list[str]) -> dict:
    """
    Function choosing desired Geojson.
    
    :param gj: initial Geojson file
    :param dzielnice: chosen districts
    :return: geojson created according to chosen districts
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

def choose_mean_df(df: DataFrame|list[DataFrame]) -> (DataFrame,list[int]):
    res_graph = []
    res_data = []
    for df in df:
        ret_dict = {"Wartość": [df.columns[1]], "Aktualna średnia": [df.iloc[:, 1].mean()]}
        res_data.append(df.iloc[:, 1].mean())
        res_graph.append(pd.DataFrame(ret_dict))
    return res_graph, res_data