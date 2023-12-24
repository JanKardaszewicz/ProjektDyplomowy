#import libraries
from graphs import *
from dash import dcc, html 
import dash_daq as daq

"""LAYOUTS"""

"""Initial/Display layout template"""
class Display_Layout(Display_Graph):  
    def __init__(self, price_range, area_range) -> None:
        super().__init__(price_range, area_range)
    def return_layout(self):
        """
        Function organising initial display layout for application
        
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
                        dcc.RangeSlider(id='price-range-slider',
                                        min=self.return_MIN_PRICE_VALUE(), max=self.return_MAX_PRICE_VALUE(), value=[self.return_MIN_PRICE_VALUE(),self.return_MAX_PRICE_VALUE()], marks=None, step = 1000,
                            tooltip={"placement": "bottom", "always_visible": True})],
                        style={"display": "inline-block", 'width': '600px', "verticalAlign": "bottom", "margin-left": "50px", "margin-right": "50px"},
                    ),
                    html.Div([html.Label('Area range:'), 
                            dcc.RangeSlider(id='area-range-slider',
                                            min=self.return_MIN_AREA_VALUE(), max=self.return_MAX_AREA_VALUE(), value=[self.return_MIN_AREA_VALUE(),self.return_MAX_AREA_VALUE()], marks=None,
                            tooltip={"placement": "bottom", "always_visible": True})],style={"display": "inline-block", 'width': '600px', "verticalAlign": "bottom"},
                )], style={"display": "inline-block","verticalAlign": "bottom", "text-align": "top", "width": "1300px","margin-top": "20px", "margin-left": "30px"})          
            ],style={"font-weight": "bold"}),      
        ])

class Analysis_Layout(Analysis_Graph): 
    def __init__(self, city_part) -> None:
        super().__init__(city_part) 
        
    """analysis layout template"""
    def return_layout(self):
        """
        Function organising analysis display layout for application
        
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