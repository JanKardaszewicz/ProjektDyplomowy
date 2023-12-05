#Project Jan Kardaszewicz 

#import libraries
from data import *
import plotly.express as px


"""Graph functions"""

def init_graph(size: str = "Powierzchnia") -> px:
    """
    Initial graph figure creation for display layout.
    
    :param size: determines what size of points on graph should be set by
    :type size: string
    :return: initial figure
    """

    fig = px.scatter_mapbox(df, lat="lat", lon="lon", size=size, color="Dzielnica", size_max=15, zoom=10.5, hover_name="Dzielnica",
            mapbox_style= MAPBOX_STYLE, width=1900, height=775, center = CRACOW_CENTER)
    
    return fig

def init_graph_udpate(fig: px, on_administrative_layer: bool = False) -> None:
    """
    Function to update initial layout figure layer.
    
    :param fig: initial figure
    :param on_administrative_layer: determines if the administrative_layout is displayed or not
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
        "name": gj["features"][0]["properties"]["nazwa"],
        "source":gj,
        "visible": on_administrative_layer}]
    })

def choropleth_graph() -> px:

    fig = px.choropleth_mapbox(mean_price_df, geojson=gj, color="srednia_cena_za_m2",
                           locations="Dzielnica",featureidkey="properties.nazwa",
                           mapbox_style=MAPBOX_STYLE, zoom=ZOOM,center = CRACOW_CENTER, labels={"name": "Dzielnica"}, width=925, height=450)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

def city_part_graph(df: DataFrame, gj: dict) -> px:
    """
    Function displaying chosen cityparts data.
    
    :param df: displayed DataFrame
    :param gj: displayed Geojson
    :return: created figure
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


def bar_price_graph(df, city_part):  
    fig = px.bar(df, x="Dzielnica", y="srednia_cena_za_m2", title="Średnia cena za metr kwardatowy względem dzielnic", height=400,width=1250)
    fig.update_traces(marker_color="blue")
    highlighted_color = "blue"
    colors = [highlighted_color if cat in city_part else "lightskyblue" for cat in df["Dzielnica"]]
    fig.update_traces(marker_color=colors)    

    return fig

def bar_area_graph(df, city_part): 
    fig = px.bar(df, x="srednia_powierzchnia", y="Dzielnica", title="Średnia powierzchnia mieszkania względem dzielnic", height=450, width=950, orientation="h")
    fig.update_traces(marker_color="indigo")
    highlighted_color = "indigo"
    colors = [highlighted_color if cat in city_part else "mediumorchid" for cat in mean_area_df["Dzielnica"]]
    fig.update_traces(marker_color=colors)
    
    return fig

def bar_mean_graph(mean_df : list[DataFrame], mean_values: list[int]) -> list[px.bar]:
    fig = px.bar(mean_df[0], x="Wartość", y= "Aktualna średnia", title=f"Średnia cena to: {mean_values[0]:.2f}", height=400,width=300)
    fig.update_yaxes(range=[0, 15000])
    fig2 = px.bar(mean_df[1], x="Wartość", y= "Aktualna średnia",color="Wartość", color_discrete_map={'Wartość': 'red'}, title=f"Średnia powierzchnia to: {mean_values[1]:.2f}", height=400,width=300)
    fig2.update_layout(showlegend=False)
    fig2.update_yaxes(range=[0, 150])
    return [fig, fig2]

"""Creating initial figures"""

display_fig = init_graph()
init_graph_udpate(display_fig)
analysys_fig = choropleth_graph()
