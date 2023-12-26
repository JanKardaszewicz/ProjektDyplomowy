#import libraries
from graphs import *
from dash import dcc, html, dash_table
import dash_daq as daq

"""LAYOUTS"""

class Display_Layout(Display_Graph):  
    """
    Class to manage Display Layout.
    """ 
    def __init__(self, price_range: list[float], area_range:list[float]) -> None:
        """
        Init function to initialize Display_Graph instance.

        Args:
            price_range (list[float]): chosen price range
            area_range (list[float]): chosen area range
        """
        super().__init__(price_range, area_range)
    def return_layout(self):
        """
        Function organising initial display layout for application.
        
        Returns:
            html.Div: initial layout
        """
        return html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(
                    figure = self.initial_display()
                    )], id="initial_layout", style={"display": "inline-block","margin-right": "10px", "margin-top": "10px"}
                ),],
            ),
            html.Div(
            [
                html.Div([
                daq.ToggleSwitch(
                    id="administrative_layout_switch", value=False, color="red",label="Podział administracyjny na dzielnice",
                    labelPosition="top")], style={"display": "inline-block", "margin-right": "10px", "verticalAlign": "bottom", "text-align": "bottom","margin-left": "0px", "width": "275px", "margin-top": "20px"}
                ),
                html.Div(
                    id="administrative_layout_switch_output-text", style={"display": "inline-block", "text-align": "center", "width": "20px", "margin-top": "10px", "margin-left": "-110px"}
                ),
                html.Div([
                    daq.ToggleSwitch(
                        id="points_size_switch",
                        value=False,
                        color=None,
                        label="Rozmiar punktów określa:",
                        labelPosition="top"
                    )], style={"display": "inline-block","verticalAlign": "top", "text-align": "top", "width": "200px", "margin-top": "25px", "margin-left": "50px"}
                ),
                html.Div(
                    id="points_size_switch_output-text", style={"display": "inline-block", "verticalAlign": "middle", "width": "50px", "margin-left": "-60px", "margin-bottom": "5px"}
                ),
                html.Div(
                    [html.Div([html.Label("Price range:"),
                        dcc.RangeSlider(id="price-range-slider",
                                        min=self.return_MIN_PRICE_VALUE(), max=self.return_MAX_PRICE_VALUE(), value=[self.return_MIN_PRICE_VALUE(),self.return_MAX_PRICE_VALUE()], marks=None, step = 1000,
                            tooltip={"placement": "bottom", "always_visible": True})],
                        style={"display": "inline-block", "width": "600px", "verticalAlign": "bottom", "margin-left": "50px", "margin-right": "50px"},
                    ),
                    html.Div([html.Label("Area range:"), 
                            dcc.RangeSlider(id="area-range-slider",
                                            min=self.return_MIN_AREA_VALUE(), max=self.return_MAX_AREA_VALUE(), value=[self.return_MIN_AREA_VALUE(),self.return_MAX_AREA_VALUE()], marks=None,
                            tooltip={"placement": "bottom", "always_visible": True})],style={"display": "inline-block", "width": "600px", "verticalAlign": "bottom"},
                )], style={"display": "inline-block","verticalAlign": "bottom", "text-align": "top", "width": "1300px","margin-top": "20px", "margin-left": "30px"})          
            ],style={"font-weight": "bold"}),      
        ])


class Analysis_Layout(Analysis_Graph):
    """
    Class to manage Analysis Layout.
    """ 
    def __init__(self, city_part: list[str]) -> None:
        """
        Init funciton to initialize Analysis Graph instance.

        Args:
            city_part (list[str]): chosen city parts
        """
        super().__init__(city_part) 
        
    def return_layout(self):
        """
        Function organising analysis display layout for application.
        
        Returns:
            html.Div: analysis layout
        """
        return html.Div([
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
                options=self.districts,
                value=[],
                inline=True,
            ),                 
            ]),
            html.Div([
                dcc.Graph(
                figure = self.choropleth_graph()
                )], id="analysis_layout", style={"display": "inline-block",  "margin-top": "10px"}
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
        
class Modify_Layout(Modify_Data):
    """
    Class to manage Modify Application Layout.
    """
    def __init__(self):
        """
        Function to initialize Modify Data.
        """
        super().__init__()
        self.df = self.DF.loc[:, ["Dzielnica", "Cena","Ulica", "Powierzchnia", "Cena_za_m2"]]

    def return_layout(self):
        """
        Function organising Modify Layout for Application.

        Returns:
            html.Div: Modify Layout
        """
        return html.Div([
            html.Div(
            [
                html.I("Podaj dane dodawanej inwestycji:", style={"font-size": "25px"}),
                html.Br(style={"line-height": "10px"}),
                html.I("Dzielnica: "),
                dcc.Input(id="input_dzielnica", type="text", placeholder="", debounce=True, style={"marginRight":"10px", "margin-bottom": "20px", "margin-top": "20px", "width": "200px"}),
                html.Br(style={"line-height": "10px"}),
                html.I("Ulica: "),
                dcc.Input(id="input_ulica", type="text", placeholder="", debounce=True, style={"marginRight":"10px", "margin-bottom": "20px", "margin-top": "10px", "width": "225px"}),
                html.Br(style={"line-height": "10px"}),
                html.I("Cena [PLN]: ", style={"margin-right": "100px"}),
                html.I("Powierzchnia [m²]: "),
                html.Br(style={"line-height": "10px"}),
                dcc.Input(id="input_cena", type="number", placeholder="", debounce=True, style={"marginRight":"80px", "margin-bottom": "20px", "margin-top": "10px", "width": "100px"}),
                dcc.Input(id="input_powierzchnia", type="number", placeholder="", debounce=True, style={"marginRight":"10px", "margin-bottom": "10px", "width":"50px"}),
                html.Div(id="output-container"),
                html.Button("Add", id="submit-button", n_clicks=0, style={"width": "75px", "height":"30px", "marginLeft" : "275px"}),
            ],style={"display": "inline-block","vertical-align":"top", "width": "20%", "margin-left": "10px", "margin-right": "10px", "font-weight": "bold", "margin-top": "50px"},),
            html.Div([
                html.I("Dostępne dane", style={"font-size": "25px","font-weight": "bold"}),
                html.Br(),
                dash_table.DataTable(self.df.to_dict("records"), [{"name": i, "id": i} for i in self.df.columns],
                                     page_size=22,
                                     filter_action="native",
                                     id="datatable",
                                    )
            ], style={"display": "inline-block", "width": "77%", "margin-left": "10px"})
        ])