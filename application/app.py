#Project Jan Kardaszewicz 

#import libraries
from graphs import *
from dash import Dash, dcc, html, Input, Output, callback_context
import dash_daq as daq
from typing import Tuple

"""LAYOUTS"""

"""Initial/Display layout template"""
initial_layout = html.Div([
    html.Div([
        html.Div([
            dcc.Graph(
            figure = display_fig
            )], id="initial_layout", style={"display": "inline-block","margin-right": "10px", "margin-top": "10px"}
        ),],
    ),
    html.Div(
    [
        html.Div([
            html.Div([
            daq.ToggleSwitch(
                id="administrative_layout_switch", value=False, color="red",label="Podział administracyjny na dzielnice",
                labelPosition="top")], style={"display": "inline-block", "margin-right": "10px", "verticalAlign": "bottom", "text-align": "bottom","margin-left": "0px", "width": "275px", "margin-top": "10px"}
            ),
            html.Div(
                id="administrative_layout_switch_output-text", style={"display": "inline-block", "text-align": "center", "width": "20px", "margin-top": "10px", "margin-left": "-110px"}
            ),
            html.Div([
                daq.ToggleSwitch(
                    id="points_size_switch",
                    value=False,
                    color="red",
                    label="Size of points",
                    labelPosition="top"
                )], style={"display": "inline-block","verticalAlign": "bottom", "text-align": "top", "width": "200px", "margin-top": "20px", "margin-left": "50px"}
            ),
            html.Div(
                id="points_size_switch_output-text", style={"display": "inline-block", "verticalAlign": "middle", "width": "50px", "margin-left": "-50px", "margin-bottom": "5px"}
            ),
        ],),
    ],),       
])

"""Analysys layout template"""
analysys_layout = html.Div([
        html.Div([
        html.Label(["Wyświetlane dzielnice:"], style={"font-weight": "bold", "text-align": "center"}),  
        dcc.Checklist(
            id="all-checklist",
            options=["Wszystkie"],
            value=[],
            inline=True,
        ),
        dcc.Checklist(
            id="districts-checklist",
            options=districts,
            value=[],
            inline=True,
        ),                 
        ]),
        html.Div([
            dcc.Graph(
            figure = analysys_fig
            )], id="analysys_layout", style={"display": "inline-block",  "margin-top": "10px"}
        ),
        html.Div([
            dcc.Graph(
            id="bar_avg_area"
            )], style={"display": "inline-block",  "margin-top": "10px"}
        ),
        html.Div([
            dcc.Graph(id="bar_mean_price")
        ], style={"display": "inline-block",  "margin-left": "0"}),
        html.Div([
            dcc.Graph(id="bar_mean_area")
        ], style={"display": "inline-block",  "margin-left": "0"}),
        html.Div([
            dcc.Graph(id="bar_avg_price_for_m2")
        ], style={"display": "inline-block",  "margin-left": "0"}),
        
    ])


"""START APP"""

"""app with common elements for all layouts"""

app = Dash(__name__, suppress_callback_exceptions=True)
app.layout = html.Div([
    html.Div([
        html.Label(["Rodzaj wyświetlania:"], style={"font-weight": "bold", "text-align": "center"}),
        dcc.Dropdown(["Display", "Analysys"], "Display", id="display-dropdown"),    
    ]),
    html.Div(id="current-layout"),
])


"""APP CALLBACKS"""

"""MAIN CALLBACK"""

"""Changing layout callback"""

@app.callback(
    Output("current-layout", "children"),
    Input("display-dropdown", "value"),
)

def display_layout(display_type: str) -> html:
    """
    Callback function changing displayed layout according to dropdown values.

    :param display_type: determines what type of layout should be displayed
    :return: updated layout
    """
    if display_type == "Display":
        return initial_layout
    if display_type == "Analysys":
        return  analysys_layout


"""DISPLAY CALLBACK"""

@app.callback(
    Output("initial_layout", "children"),
    Input("administrative_layout_switch", "value"),
    Input("points_size_switch", "value"),
)

def update_output(on_administrative_layer: bool, size_switch_value: bool) -> dcc:
    """
    Callback function changing graph according to switches values.

    :param on_administrative_layer: determines if administrative_layer is on or off
    :param size_switch_value: determines if size of points is set by Price or Area
    :return: updated graph 
    """
    if size_switch_value:
        fig = init_graph(size="Cena")
    else:
        fig = init_graph(size="Powierzchnia")
        
    init_graph_udpate(fig, on_administrative_layer)

    return [dcc.Graph(figure=fig)]


@app.callback( 
    Output("points_size_switch_output-text", "children"),
    Input("points_size_switch", "value"),
)

def display_text(value: bool) -> str:
    """
    Callback function displaying text according to switch value.

    :param value: value of switch
    :return: text text if the size of points is determined by Price or Area
    """

    if value:
        return "Cena"
    else:
        return "Powierzchnia"


@app.callback( 
    Output("administrative_layout_switch_output-text", "children"),
    Input("administrative_layout_switch", "value"),
) 

def display_text2(value: bool) -> str:
    """
    Callback function displaying text according to switch value.

    :param value: value of switch
    :return: text if the administrative_layout is displayed or not
    """
    if value:
        return "On"
    else:
        return "Off"


"""ANALYSYS CALLBACK"""

@app.callback(
    Output("districts-checklist", "value"),
    Output("all-checklist", "value"),
    Input("districts-checklist", "value"),
    Input("all-checklist", "value"),
)
def sync_checklists(districts_selected: list[str], all_selected: list[str]) -> Tuple[list[str], list[str]]:
    """
    Callback function to sync 'Wszystkie' button in checklists with all the others.

    :param districts_selected: all parts of Kraków selected in checklist
    :param all_selected: button sellecting all parts of Krakow if all parts are selected this button is selected automaticly.
    :return: checked values of checklists 
    """

    ctx = callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if input_id == "districts-checklist":
        all_selected = ["Wszystkie"] if set(districts_selected) == set(districts) else []
    else:
        districts_selected = districts if all_selected else []
    return districts_selected, all_selected


@app.callback(
    Output("analysys_layout", "children"),
    Output("bar_avg_price_for_m2", "figure"),
    Output("bar_avg_area", "figure"),
    Output("bar_mean_price", "figure"),
    Output("bar_mean_area", "figure"),
    [Input("districts-checklist", "value")],
    [Input("all-checklist", "value")],
)

def change_displayed_city_part(city_part: list[str], check_all: list[str]) -> dcc:
    """
    Callback function to sync checklists with the graphs.

    :param city_part: all parts of Kraków selected in checklist
    :param check_all: button sellecting all parts of Krakow if all parts are selected this button is selected automaticly.
    :return: figures set accordingly to checklists checked values
    """

    analysys_fig = choropleth_graph()
    bar_avg_price = bar_price_graph(mean_price_df, city_part)
    bar_avg_area = bar_area_graph(mean_area_df, city_part)
    mean_df, mean_values = choose_mean_df([mean_price_df,mean_area_df])
    mean_figs = bar_mean_graph(mean_df, mean_values)

    if check_all:
        return [dcc.Graph(figure=analysys_fig), bar_avg_price, bar_avg_area, mean_figs[0], mean_figs[1]]
    
    else:
        new_df = choose_df(df, city_part)
        new_gj = choose_gj(gj, city_part)
        new_mean_price_df = choose_df(mean_price_df, city_part)
        new_mean_area_df = choose_df(mean_area_df,city_part)
        mean_df, mean_values = choose_mean_df([new_mean_price_df,new_mean_area_df])

        analysys_fig = city_part_graph(df= new_df, gj= new_gj)
        mean_figs = bar_mean_graph(mean_df, mean_values)


    return [dcc.Graph(figure=analysys_fig), bar_avg_price, bar_avg_area, mean_figs[0], mean_figs[1]]


if __name__ == "__main__":
    app.run_server(debug=True)