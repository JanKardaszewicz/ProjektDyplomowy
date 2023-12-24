#Project Jan Kardaszewicz 
from layouts import *
from dash import Dash, Input, Output, callback_context

"""START APP"""
Data = Data_Prep()
"""app with common elements for all layouts"""

app = Dash(__name__, suppress_callback_exceptions=True)
app.layout = html.Div([
    html.Div([
        html.Label(["Rodzaj wyświetlania:"], style={"font-weight": "bold", "text-align": "center"}),
        dcc.Dropdown(["Wizualizacja", "Analiza"], "Wizualizacja", id="display-dropdown"),    
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

def display(display_type: str):
    """
    Callback function changing displayed layout according to dropdown values.

    :param display_type: determines what type of layout should be displayed
    :type display_type: str

    Returns:
        dash.html: updated layout
    """
    if display_type == "Wizualizacja":
        return Display_Layout(price_range=[Data.return_MIN_PRICE_VALUE(), Data.return_MAX_PRICE_VALUE()], area_range = [Data.return_MIN_AREA_VALUE(), Data.return_MAX_AREA_VALUE( )]).return_layout()
    if display_type == "Analiza":
        return Analysis_Layout(city_part=[]).return_layout()


"""DISPLAY CALLBACK"""

@app.callback(
    Output("initial_layout", "children"),
    Input("administrative_layout_switch", "value"),
    Input("points_size_switch", "value"),
    Input("price-range-slider", "value"),
    Input("area-range-slider", "value")
)

def update_output(on_administrative_layer: bool, size_switch_value: bool, price_range: list[float], area_range: list[float]):
    """
    Callback function changing graph according to switches values.

    :param on_administrative_layer: determines if administrative_layer is on or off
    :type on_administrative_layer: bool
    :param size_switch_value: determines if size of points is set by Price or Area
    :type size_switch_value: bool

    Returns:
        dash.dcc: updated graph 
    """
    df = Display_Graph(price_range=price_range, area_range=area_range)
    if size_switch_value:
        fig = df.initial_display(size="Cena", on_administrative_layer=on_administrative_layer)
    else:
        fig = df.initial_display(size="Powierzchnia", on_administrative_layer=on_administrative_layer)

    return [dcc.Graph(figure=fig)]


@app.callback( 
    Output("points_size_switch_output-text", "children"),
    Input("points_size_switch", "value"),
)

def display_text(value: bool):
    """
    Callback function displaying text according to switch value.

    :param value: value of switch
    :type value: bool

    Returns:
        str:  text text if the size of points is determined by Price or Area
    """

    if value:
        return "Cena"
    else:
        return "Powierzchnia"


@app.callback( 
    Output("administrative_layout_switch_output-text", "children"),
    Input("administrative_layout_switch", "value"),
) 

def display_text2(value: bool):
    """
    Callback function displaying text according to switch value.

    :param value: value of switch
    :type value: bool

    Returns:
        str: text if the administrative_layout is displayed or not
    """
    if value:
        return "On"
    else:
        return "Off"

"""analysis CALLBACK"""

@app.callback(
    Output("districts-checklist", "value"),
    Output("all-checklist", "value"),
    Input("districts-checklist", "value"),
    Input("all-checklist", "value"),
)
def sync_checklists(districts_selected: list[str], all_selected: list[str]):
    """
    Callback function to sync 'Wszystkie' button in checklists with all the others.

    :param districts_selected: all parts of Kraków selected in checklist
    :type districts_selected: list[str]
    :param all_selected: button sellecting all parts of Krakow if all parts are selected this button is selected automaticly.
    :type all_selected: list[str]

    Returns:
        Touple[list[str], list[str]: checked values of both checklists 
    """

    ctx = callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if input_id == "districts-checklist":
        all_selected = ["Wszystkie"] if set(districts_selected) == set(Data.return_districts()) else []
    else:
        districts_selected = Data.return_districts() if all_selected else []
    return districts_selected, all_selected


@app.callback(
    Output("analysis_layout", "children"),
    Output("bar_avg_price_for_m2", "figure"),
    Output("bar_avg_area", "figure"),
    Output("bar_mean_price", "figure"),
    Output("bar_mean_area", "figure"),
    [Input("districts-checklist", "value")],
    [Input("all-checklist", "value")],
)

def change_displayed_city_part(city_part: list[str], check_all: list[str]):
    """
    Callback function to sync checklists with the graphs.

    :param city_part: all parts of Kraków selected in checklist
    :type city_part: list[str]
    :param check_all: button sellecting all parts of Krakow if all parts are selected this button is selected automaticly.
    :type check_all: list[str]
    
    Returns:
        List[dash.dcc, plotly.express, plotly.express, plotly.express, plotly.express]: figures set accordingly to checklists checked values
    """
    obj = Analysis_Graph(city_part)

    if check_all:
        return [dcc.Graph(figure=obj.choropleth_graph()), obj.bar_price_graph(), obj.bar_area_graph(), obj.bar_mean_graph_area(), obj.bar_mean_graph_price()]
    
    else:    
        return [dcc.Graph(figure=obj.city_part_graph()), obj.bar_price_graph(), obj.bar_area_graph(), obj.bar_mean_graph_area(),  obj.bar_mean_graph_price()]
        

    


if __name__ == "__main__":
    app.run_server(debug=True)