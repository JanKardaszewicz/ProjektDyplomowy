#Project Jan Kardaszewicz 

#import libraries
from data_prep import *
import plotly.express as px


"""Graph functions"""

def init_graph(df: DataFrame, size: str = "Powierzchnia"):
    """
    Initial graph figure creation for display layout.
    
    :param size: determines what size of points on graph should be set by
    :type size: string, optional

    Returns:
        plotly.express: initial figure
    """

    fig = px.scatter_mapbox(df, lat="lat", lon="lon", size=size, color="Dzielnica", size_max=15, zoom=10.5, hover_name="Dzielnica",
            mapbox_style= MAPBOX_STYLE, width=1900, height=775, center = CRACOW_CENTER)
    
    return fig

def init_graph_udpate(fig, on_administrative_layer: bool = False):
    """
    Function to update initial layout figure layer.
    
    :param fig: initial figure
    :type fig: plotly.express
    :param on_administrative_layer: determines if the administrative_layout is displayed or not
    :type on_administrative_layer: bool, optional
    
    Retruns:
        None: Update layout of existing figure globaly
    """

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_layout(mapbox={
        "layers": [{
        "sourcetype": "geojson",
        "type": "fill",
        "opacity": 0.2,
        "fill":{"outlinecolor":"blue"},
        "color": "royalblue",
        "below": "traces",
        "name": MAIN_GJ["features"][0]["properties"]["nazwa"],
        "source":MAIN_GJ,
        "visible": on_administrative_layer}]
    })

def choropleth_graph():
    """Initial analysys layout graph

    Returns:
        plotly.express: choropleth graph
    """

    fig = px.choropleth_mapbox(mean_price_df, geojson=MAIN_GJ, color="srednia_cena_za_m2",
                           locations="Dzielnica",featureidkey="properties.nazwa",
                           mapbox_style=MAPBOX_STYLE, zoom=ZOOM,center = CRACOW_CENTER, labels={"name": "Dzielnica"}, width=925, height=450)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

def city_part_graph(df: DataFrame, gj: dict):
    """
    Function displaying chosen cityparts data.
    
    :param df: displayed DataFrame
    :type df: DataFrame
    :param gj: displayed Geojson
    :type gj: dict

    Returns:
        plotly.express: created figure
    """

    fig = px.scatter_mapbox(df , lat="lat", lon="lon", size="Cena", color="Dzielnica", size_max=15, zoom=10.2, hover_name="Dzielnica",
            mapbox_style= MAPBOX_STYLE, width=925, height=450, center = CRACOW_CENTER)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, showlegend=False)
    fig.update_layout(mapbox={
                "layers": [{
                "sourcetype": "geojson",
                "type": "fill",
                "opacity": 0.2,
                "fill":{"outlinecolor":"blue"},
                "color": "royalblue",
                "below": "traces",
                "source":gj,
                "visible": True}]
            })
    return fig


def bar_price_graph(df: DataFrame, city_part: list[str]): 
    """
    Function displaying bar graph of mean price for district

    :param df: DataFrame instance
    :type df: DataFrame
    :param city_part: chosen districts
    :type city_part: list[str]

    Returns:
        plotly.express: Bar graph
    """
    fig = px.bar(df, x="Dzielnica", y="srednia_cena_za_m2", title="Średnia cena za metr kwardatowy względem dzielnic", height=400,width=1250)
    fig.update_traces(marker_color="blue")
    highlighted_color = "blue"
    colors = [highlighted_color if cat in city_part else "lightskyblue" for cat in df["Dzielnica"]]
    fig.update_traces(marker_color=colors)    

    return fig

def bar_area_graph(df, city_part): 
    """Function displaying bar graph of mean area for district

    :param df: DataFrame instance
    :type df: DataFrame
    :param city_part: chosen districts
    :type city_part: list[str]

    Returns:
        plotly.express: Bar graph
    """
    fig = px.bar(df, x="srednia_powierzchnia", y="Dzielnica", title="Średnia powierzchnia mieszkania względem dzielnic", height=450, width=950, orientation="h")
    fig.update_traces(marker_color="indigo")
    highlighted_color = "indigo"
    colors = [highlighted_color if cat in city_part else "mediumorchid" for cat in mean_area_df["Dzielnica"]]
    fig.update_traces(marker_color=colors)
    
    return fig

def bar_mean_graph(mean_df : list[DataFrame], mean_values: list[int]):
    """
    Function displaying bar graph of combined mean price and area for every chosen district

    :param df: DataFrame instances in list
    :type df: list[DataFrame]
    :param city_part: chosen districts
    :type city_part: list[str]

    Returns:
        list[plotly.express]: Bar graphs for  combined mean price and area 
    """
    fig = px.bar(mean_df[0], x="Wartość", y= "Aktualna średnia", title=f"Średnia cena: {mean_values[0]:.2f} [zł/m²]", height=400,width=300)
    fig.update_yaxes(range=[0, 15000])
    fig2 = px.bar(mean_df[1], x="Wartość", y= "Aktualna średnia",color="Wartość", color_discrete_map={'Wartość': 'red'},title=f"Średnia powierzchnia: {mean_values[1]:.2f} [m²]" , height=400,width=300)
    fig2.update_layout(showlegend=False)
    fig2.update_yaxes(range=[0, 150])
    return [fig, fig2]

"""Creating initial figures"""

display_fig = init_graph(MAIN_DF)
init_graph_udpate(display_fig)
analysys_fig = choropleth_graph()
