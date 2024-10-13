import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, callback, dcc, html
from data_utils import number_of_countries, number_of_restaurants, top_cuisine
from graphs import graph_top_cuisine
from utils import apply_style_to_fig

dash.register_page(__name__, path="/")

layout = [
    html.H3("Home", className="mb-3"),
    html.P(
        """The Michelin Guide has long been synonymous with culinary excellence,
        serving as a global benchmark for top-tier dining experiences. This dashboard explores
        the data from this guide, to provide some insights and maybe make a recommendation or two!
        """
    ),
    dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4(
                                "-",
                                id="home-number-of-countries",
                                className="card-title",
                            ),
                            html.H6("Number of countries", className="card-subtitle"),
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
                                id="home-number-of-restaurants",
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
                            html.H4("-", id="home-top-cuisine", className="card-title"),
                            html.H6("Top cuisine", className="card-subtitle"),
                        ]
                    ),
                )
            ),
        ]
    ),
    dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4("Top countries"),
                            html.P("Countries with the most restaurants in the Michelin Guide."),
                            dcc.Graph(
                                id="home-graph-top-countries",
                                # Due to https://github.com/plotly/plotly.py/issues/3441
                                figure=go.Figure(layout=dict(template="plotly")),
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
                                id="home-graph-top-cuisine",
                                # Due to https://github.com/plotly/plotly.py/issues/3441
                                figure=go.Figure(layout=dict(template="plotly")),
                            ),
                        ]
                    )
                ),
                width=6,
            ),
        ],
        class_name="mt-3",
    ),
]


@callback(
    [
        Output("home-number-of-countries", "children"),
        Output("home-number-of-restaurants", "children"),
        Output("home-top-cuisine", "children"),
    ],
    Input("store", "data"),
)
def update_numbers(df):
    """Callback to update numbers on the top of homepage."""
    df = pd.DataFrame.from_dict(df)

    return (
        number_of_countries(df),
        number_of_restaurants(df),
        top_cuisine(df),
    )


@callback(
    Output("home-graph-top-countries", "figure"),
    Input("store", "data"),
)
def graph_top_countries(df_dict: dict) -> go.Figure:
    """Graph the top x countries in the dataset."""
    df_top_countries = pd.DataFrame.from_dict(df_dict)

    fig_top_countries = px.bar(
        df_top_countries["Country"].value_counts()[:10].reset_index(),
        x="Country",
        y="count",
        labels={"count": "Number of restaurants"},
    )

    fig_top_countries = apply_style_to_fig(fig_top_countries)
    return fig_top_countries


@callback(
    Output("home-graph-top-cuisine", "figure"),
    Input("store", "data"),
)
def home_graph_top_cuisine(df_dict: dict) -> go.Figure:
    """Graph the top x cuisines in the dataset."""
    df_top_cuisines = pd.DataFrame.from_dict(df_dict)

    return graph_top_cuisine(df_top_cuisines)
