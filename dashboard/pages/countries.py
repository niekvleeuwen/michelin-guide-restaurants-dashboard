import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, callback, dcc, html

from dashboard.caching import retrieve_data
from dashboard.data.utils import number_of_cities, number_of_restaurants, top_cuisine, unique_countries
from dashboard.decorators import filter_by_country, load_df
from dashboard.graphs.graphs import (
    graph_award_distribution,
    graph_map,
    graph_top_cities,
    graph_top_cuisine,
)
from dashboard.utils import TITLE

PAGE_TITLE = "Countries"

dash.register_page(__name__, name=PAGE_TITLE, title=f"{PAGE_TITLE} | {TITLE}", order=1)


def layout():
    df = retrieve_data()
    return [
        html.H3("Countries", className="mb-3"),
        html.P(
            """Visualize data per country.
        """
        ),
        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    sorted(unique_countries(df)), value="France", clearable=False, id="country-dropdown-selection"
                ),
                md=3,
                sm=12,
            ),
            class_name="mt-1",
        ),
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
                    ),
                    class_name="mb-3",
                    md=4,
                    sm=12,
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
                    ),
                    class_name="mb-3",
                    md=4,
                    sm=12,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("-", id="countries-top-cuisine", className="card-title"),
                                html.H6("Top cuisine", className="card-subtitle"),
                            ]
                        ),
                    ),
                    class_name="mb-3",
                    md=4,
                    sm=12,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Map"),
                                html.P("A map showing the location of Michelin-starred restaurants."),
                                dcc.Graph(id="countries-map-graph-content"),
                            ]
                        )
                    ),
                    class_name="mb-3",
                    width=12,
                ),
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
                    class_name="mb-3",
                    md=6,
                    sm=12,
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
                    class_name="mb-3",
                    md=6,
                    sm=12,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Award distribution"),
                                html.P("Breakdown of distribution of Michelin ratings."),
                                dcc.Graph(id="countries-graph-awards-distribution"),
                            ]
                        )
                    ),
                    class_name="mb-3",
                    md=6,
                    sm=12,
                ),
                dbc.Col([], class_name="mb-3", md=6, sm=0),
            ],
            class_name="g-3",
        ),
    ]


@callback(
    [
        Output("countries-number-of-cities", "children"),
        Output("countries-number-of-restaurants", "children"),
        Output("countries-top-cuisine", "children"),
        Output("countries-map-graph-content", "figure"),
        Output("countries-graph-top-cities", "figure"),
        Output("countries-graph-top-cuisine", "figure"),
        Output("countries-graph-awards-distribution", "figure"),
    ],
    [
        Input("country-dropdown-selection", "value"),
    ],
)
@load_df
@filter_by_country
def update_numbers(df: pd.DataFrame):
    """Callback to update numbers on the top of homepage."""
    return (
        number_of_cities(df),
        number_of_restaurants(df),
        top_cuisine(df),
        graph_map(df),
        graph_top_cities(df),
        graph_top_cuisine(df),
        graph_award_distribution(df),
    )
