import dash
import dash_bootstrap_components as dbc
import pandas as pd
from caching import retrieve_data
from dash import Input, Output, callback, dcc, html
from data.utils import unique_countries
from decorators import filter_by_country, load_df
from graphs.graphs import (
    graph_heatmap_price,
    graph_price_distribution,
    graph_scatter_best_value,
)
from utils import TITLE

PAGE_TITLE = "Pricing"

dash.register_page(__name__, name=PAGE_TITLE, title=f"{PAGE_TITLE} | {TITLE}", order=2)


def layout():
    df = retrieve_data()
    return [
        html.H3("Pricing", className="mb-3"),
        html.P(
            """This page provides an overview of pricing,
        showcasing the distribution of Michelin Guide restaurants across different price categories.
        """
        ),
        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    sorted(unique_countries(df)),
                    value="France",
                    clearable=False,
                    id="pricing-country-dropdown-selection",
                ),
                width=3,
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
                                html.H4("Price Distribution"),
                                html.P(" Number of restaurants in each price category."),
                                dcc.Graph(id="pricing-graph-price-distribution"),
                            ]
                        ),
                    )
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Heatmap"),
                                html.P("Heatmap of Michelin Award by price category."),
                                dcc.Graph(id="pricing-graph-heatmap"),
                            ]
                        ),
                    )
                ),
            ],
            class_name="mt-4",
        ),
        dbc.Row(
            dbc.Col(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Best value"),
                                html.P(
                                    [
                                        """This plot shows how Michelin Guide restaurants in different price categories
                                    align with their awards""",
                                        html.Span(
                                            html.I(className="bi bi-info-circle ml-2"),
                                            id="pricing-best-value-tooltip-target",
                                            style={"cursor": "pointer"},
                                        ),
                                        dbc.Tooltip(
                                            """
                                    A higher award at a lower price indicates better value.
                                    """,
                                            target="pricing-best-value-tooltip-target",
                                        ),
                                        ".",
                                    ]
                                ),
                                dcc.Graph(id="pricing-best-value-scatter"),
                            ]
                        ),
                    )
                ],
                width=12,
            ),
            class_name="mt-4",
        ),
    ]


@callback(
    [
        Output("pricing-graph-price-distribution", "figure"),
        Output("pricing-best-value-scatter", "figure"),
        Output("pricing-graph-heatmap", "figure"),
    ],
    [
        Input("pricing-country-dropdown-selection", "value"),
    ],
)
@load_df
@filter_by_country
def update_price_distribution(df: pd.DataFrame):
    """Update the price distribution graph."""
    return (graph_price_distribution(df), graph_scatter_best_value(df), graph_heatmap_price(df))
