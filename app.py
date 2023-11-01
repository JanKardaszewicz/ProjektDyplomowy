#Project Jan Kardaszewicz 

#import libraries

import plotly.express as px
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import dash_daq as daq
import json 

"""DATA PREPARATION"""

"""Constants"""
CRACOW_CENTER = {"lat": 50.049683, "lon": 19.984544}
MAPBOX_STYLE = "carto-positron"
ZOOM = 10

"""Getting geo data"""

df = pd.read_csv("mieszkania.csv", sep=';')
with open('Dzielnice_administracyjne2.geojson',encoding="utf8") as f:
    gj = json.load(f)

df2 = pd.read_csv('mieszkania_srednia.csv')
df2['srednia_cena_za_m2'] = pd.to_numeric(df2['srednia_cena_za_m2'])


df3 = pd.read_csv('mieszkania_powierzchnia.csv')
df3['srednia_powierzchnia'] = pd.to_numeric(df3['srednia_powierzchnia'])

df_StareMiasto = df.loc[df["Dzielnica"] == "Stare Miasto"]
gj_StareMiasto = gj['features'][0]

df_Grzegorzki = df.loc[df["Dzielnica"] == "Grzegórzki"]
gj_Grzegorzki = gj['features'][1]

"""Graph functions"""

def init_graph(size= "Powierzchnia"):
    """Initial layout figure creation"""

    fig = px.scatter_mapbox(df, lat="lat", lon="lon", size=size, color="Dzielnica", size_max=15, zoom=10.5, hover_name="Dzielnica",
            mapbox_style= MAPBOX_STYLE, width=1900, height=775, center = CRACOW_CENTER)
    
    return fig

def init_graph_udpate(fig, on_administrative_layer= False):
    """Function to update initial layout figure layers"""

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_layout(mapbox={
        'layers': [{
        "sourcetype": "geojson",
        "type": "fill",
        "opacity": 0.2,
        "fill":{"outlinecolor":"blue"},
        "color": "royalblue",
        "below": "traces",
        "name": gj['features'][0]['properties']['nazwa'],
        "source":gj,
        "visible": on_administrative_layer}]
    })

def choropleth_graph():
    fig = px.choropleth_mapbox(df2, geojson=gj, color='srednia_cena_za_m2',
                           locations='Dzielnica',featureidkey="properties.nazwa",
                           mapbox_style=MAPBOX_STYLE, zoom=ZOOM,center = CRACOW_CENTER, labels={"name": "Dzielnica"}, width=925, height=450)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


def city_part_graph(df, gj, center):
    fig = px.scatter_mapbox(df , lat="lat", lon="lon", size="Cena", color="Dzielnica", size_max=15, zoom=12, hover_name="Dzielnica",
            mapbox_style= MAPBOX_STYLE, width=925, height=450, center = center)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, showlegend=False)
    fig.update_layout(mapbox={
                'layers': [{
                "sourcetype": "geojson",
                "type": "fill",
                "opacity": 0.2,
                "fill":{"outlinecolor":"blue"},
                "color": "royalblue",
                "below": "traces",
                "name": gj['properties']['nazwa'],
                "source":gj,
                "visible": True}]
            })
    return fig


"""Creating initial figure"""
fig = init_graph()
init_graph_udpate(fig)
fig2 = choropleth_graph()

"""LAYOUTS"""

"""different layouts projects"""
initial_layout = html.Div([
    html.Div([
        html.Div([
            dcc.Graph(
            figure = fig
            )], id="initial_layout", style={'display': 'inline-block','margin-right': '10px', 'margin-top': '10px'}
        ),],
    ),
    html.Div(
    [
        html.Div([
            html.Div([
            daq.ToggleSwitch(
                id="administrative_layout_switch", value=False, color="red",label="Podział administracyjny na dzielnice",
                labelPosition="top")], style={'display': 'inline-block', 'margin-right': '10px', 'verticalAlign': 'bottom', 'text-align': 'bottom','margin-left': '0px', 'width': '275px', 'margin-top': '10px'}
            ),
            html.Div(
                id='administrative_layout_switch_output-text', style={'display': 'inline-block', 'text-align': 'center', 'width': '20px', 'margin-top': '10px', 'margin-left': '-110px'}
            ),
            html.Div([
                daq.ToggleSwitch(
                    id='points_size_switch',
                    value=False,
                    color="red",
                    label="Size of points",
                    labelPosition="top"
                )], style={'display': 'inline-block','verticalAlign': 'bottom', 'text-align': 'top', 'width': '200px', 'margin-top': '20px', 'margin-left': '50px'}
            ),
            html.Div(
                id='points_size_switch_output-text', style={'display': 'inline-block', 'verticalAlign': 'middle', 'width': '50px', 'margin-left': '-50px', 'margin-bottom': '5px'}
            ),
        ],),
    ],),       
])

analysys_layout = html.Div([
        html.Div([
        html.Label(["Wyświetlane dzielnice:"], style={'font-weight': 'bold', "text-align": "center"}),
        dcc.Dropdown(["Wszystkie","Stare Miasto", "Grzegórzki"], "Wszystkie", id='city_parts_dropdown'),    
        ]),
        html.Div([
            dcc.Graph(
            figure = fig2
            )], id="analysys_layout", style={'display': 'inline-block',  'margin-top': '10px'}
        ),
        html.Div([
            dcc.Graph(
            id="bar_avg_area"
            )], style={'display': 'inline-block',  'margin-top': '10px'}
        ),
        html.Div([
            dcc.Graph(id='bar_avg_price_for_m2')
        ])
    ])

"""START APP"""

"""app with common elements for all layouts"""

app = Dash(__name__, suppress_callback_exceptions=True)
app.layout = html.Div([
    html.Div([
        html.Label(["Rodzaj wyświetlania:"], style={'font-weight': 'bold', "text-align": "center"}),
        dcc.Dropdown(["Display", "Analysys"], "Display", id='display-dropdown'),    
    ]),
    html.Div(id='current-layout'),
])


"""APP CALLBACKS"""

"""MAIN CALLBACK"""

"""Changing layout callback"""

@app.callback(
    Output('current-layout', 'children'),
    Input('display-dropdown', 'value'),
)

def display_layout(display_type):
    if display_type == "Display":
        return initial_layout
    if display_type == "Analysys":
        return  analysys_layout

"""Button callback to set administrative division layout"""
"""Dropdown callback to set sizes of markers"""

"""DISPLAY CALLBACK"""

@app.callback(
    Output("initial_layout", "children"),
    Input("administrative_layout_switch", "value"),
    Input('points_size_switch', 'value'),
)

def update_output(on_administrative_layer, size_switch_value):
    """Button and dropdown callback function"""
    if size_switch_value:
        fig = init_graph(size="Cena")
    else:
        fig = init_graph(size="Powierzchnia")
        
    init_graph_udpate(fig, on_administrative_layer)

    return [dcc.Graph(figure=fig)]

@app.callback( 
    Output('points_size_switch_output-text', 'children'),
    Input('points_size_switch', 'value'),
)

def display_text(value):
    if value:
        return "Cena"
    else:
        return "Powierzchnia"

@app.callback( 
    Output('administrative_layout_switch_output-text', 'children'),
    Input('administrative_layout_switch', 'value'),
) 
def display_text2(value):
    if value:
        return "On"
    else:
        return "Off"

"""ANALYSYS CALLBACK"""
@app.callback( 
    Output('analysys_layout', 'children'),
    Output('bar_avg_price_for_m2', 'figure'),
    Output("bar_avg_area", "figure"),
    Input('city_parts_dropdown', 'value'),
) 

def change_displayed_city_part(city_part):

    fig2 = choropleth_graph()
    bar_avg_price = px.bar(df2, x='Dzielnica', y='srednia_cena_za_m2', title='Średnia cena za metr kwardatowy względem dzielnic', height=400,)
    bar_avg_price.update_traces(marker_color="blue")
    bar_avg_area = px.bar(df3, x='srednia_powierzchnia', y='Dzielnica', title='Średnia powierzchnia mieszkania względem dzielnic', height=450, width=925, orientation='h')
    bar_avg_area.update_traces(marker_color="indigo")
    if city_part == "Stare Miasto":
        fig2 = city_part_graph(df= df_StareMiasto,gj= gj_StareMiasto, center= {"lat": 50.0619, "lon": 19.939697})

        highlighted_color = 'blue'
        colors = [highlighted_color if cat == city_part else 'lightskyblue' for cat in df2['Dzielnica']]
        bar_avg_price.update_traces(marker_color=colors)

        highlighted_color = 'indigo'
        colors = [highlighted_color if cat == city_part else 'mediumorchid' for cat in df3['Dzielnica']]
        bar_avg_area.update_traces(marker_color=colors)

    elif city_part == "Grzegórzki":
        fig2 = city_part_graph(df= df_Grzegorzki,gj= gj_Grzegorzki, center= {"lat": 50.0619, "lon": 19.939697})
        
        highlighted_color = 'blue'
        colors = [highlighted_color if cat == city_part else 'lightskyblue' for cat in df2['Dzielnica']]
        bar_avg_price.update_traces(marker_color=colors)

        highlighted_color = 'indigo'
        colors = [highlighted_color if cat == city_part else 'mediumorchid' for cat in df3['Dzielnica']]
        bar_avg_area.update_traces(marker_color=colors)

    return [dcc.Graph(figure=fig2), bar_avg_price, bar_avg_area]




if __name__ == '__main__':
    app.run_server(debug=True)