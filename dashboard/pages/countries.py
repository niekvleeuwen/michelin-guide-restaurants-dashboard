import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, callback, dcc, html

from dashboard.data.utils import number_of_cities, number_of_restaurants, top_cuisine, unique_countries
from dashboard.decorators import df_from_dict, filter_by_country
from dashboard.graphs.graphs import (
    graph_award_distribution,
    graph_map,
    graph_top_cities,
    graph_top_cuisine,
)
from dashboard.utils import TITLE

PAGE_TITLE = "Countries"

dash.register_page(__name__, name=PAGE_TITLE, title=f"{PAGE_TITLE} | {TITLE}", order=1)

layout = [
    html.H3("Countries", className="mb-3"),
    html.P(
        """Visualize data per country.
        """
    ),
    dbc.Row(dbc.Col(dcc.Dropdown([], clearable=False, id="country-dropdown-selection"), width=3), class_name="mt-1"),
    html.Hr(),
    dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4(
                                "-",
                                id="countries-number-of-cities",
                                className="card-title",
                            ),
                            html.H6("Number of cities", className="card-subtitle"),
                        ]
                    ),
                )
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4(
                                "-",
                                id="countries-number-of-restaurants",
                                className="card-title",
                            ),
                            html.H6("Number of restaurants", className="card-subtitle"),
                        ]
                    ),
                )
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4("-", id="countries-top-cuisine", className="card-title"),
                            html.H6("Top cuisine", className="card-subtitle"),
                        ]
                    ),
                )
            ),
        ],
        class_name="mt-4",
    ),
    dbc.Row(
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H4("Map"),
                        html.P("A map showing the location of Michelin-starred restaurants."),
                        dcc.Graph(id="countries-map-graph-content"),
                    ]
                )
            )
        ),
        class_name="mt-3",
    ),
    dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4("Top cities"),
                            html.P("Cities with the most restaurants in the Michelin Guide."),
                            dcc.Graph(
                                id="countries-graph-top-cities",
                            ),
                        ]
                    )
                ),
                width=6,
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4("Top cuisines"),
                            html.P("The most common cuisine types of restaurants in the Michelin Guide."),
                            dcc.Graph(
                                id="countries-graph-top-cuisine",
                            ),
                        ]
                    )
                ),
                width=6,
            ),
        ],
        class_name="mt-3",
    ),
    dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4("Award distribution"),
                            html.P("Breakdown of distribution of Michelin ratings."),
                            dcc.Graph(id="countries-awards-distribution"),
                        ]
                    )
                ),
                width=6,
            ),
            dbc.Col(
                [],
                width=6,
            ),
        ],
        class_name="mt-3",
    ),
]


@callback(
    [
        Output("country-dropdown-selection", "options"),
        Output("country-dropdown-selection", "value"),
    ],
    Input("store", "data"),
)
@df_from_dict
def update_dropdown(df):
    """Update dropdown with unique countries."""
    countries = unique_countries(df)
    default_country = "France"
    return sorted(countries), default_country


@callback(
    [
        Output("countries-number-of-cities", "children"),
        Output("countries-number-of-restaurants", "children"),
        Output("countries-top-cuisine", "children"),
    ],
    [
        Input("store", "data"),
        Input("country-dropdown-selection", "value"),
    ],
)
@df_from_dict
@filter_by_country
def update_numbers(df: pd.DataFrame):
    """Callback to update numbers on the top of homepage."""
    return (
        number_of_cities(df),
        number_of_restaurants(df),
        top_cuisine(df),
    )


@callback(
    Output("countries-graph-top-cities", "figure"),
    [
        Input("store", "data"),
        Input("country-dropdown-selection", "value"),
    ],
)
@df_from_dict
@filter_by_country
def update_graph_top_cities(df: pd.DataFrame) -> go.Figure:
    """Graph the top x cities in the dataset."""
    return graph_top_cities(df)


@callback(
    Output("countries-graph-top-cuisine", "figure"),
    [
        Input("store", "data"),
        Input("country-dropdown-selection", "value"),
    ],
)
@df_from_dict
@filter_by_country
def countries_top_cuisine(df: pd.DataFrame) -> go.Figure:
    """Graph the top x cuisines in the dataset."""
    return graph_top_cuisine(df)


@callback(
    Output("countries-awards-distribution", "figure"),
    [
        Input("store", "data"),
        Input("country-dropdown-selection", "value"),
    ],
)
@df_from_dict
@filter_by_country
def update_graph_award_distribution(df: pd.DataFrame):
    return graph_award_distribution(df)


@callback(
    Output("countries-map-graph-content", "figure"),
    [
        Input("store", "data"),
        Input("country-dropdown-selection", "value"),
    ],
)
@df_from_dict
@filter_by_country
def update_graph_map(df: pd.DataFrame):
    """Plot the locations of restaurants on a map."""
    return graph_map(df)
