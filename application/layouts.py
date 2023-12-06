#import libraries
from graphs import *
from dash import dcc, html 
import dash_daq as daq

"""LAYOUTS"""

"""Initial/Display layout template"""
def initial_layout():
    """
    Function organising initial display layout for application
    
    Returns:
        html.Div: initial layout
    """
    return html.Div([
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
def analysys_layout():
    """
    Function organising analysys display layout for application
    
    Returns:
        html.Div: analysys layout
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
