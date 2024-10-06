import dash
from dash import html
import dash_bootstrap_components as dbc
from dash import callback, Input, Output, dcc
import pandas as pd
import plotly.express as px


dash.register_page(__name__, path="/")

layout = [
    html.H3("Home", className="mb-3"),
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
                [
                    html.H4("Top countries"),
                    html.P("Countries with the most restaurants in the Michelin Guide."),
                    dcc.Graph(id="home-graph-top-countries"),
                ],
                width=6,
            ),
            dbc.Col(
                [
                    html.H4("Top cuisines"),
                    html.P("The most common cuisine types of restaurants in the Michelin Guide."),
                    dcc.Graph(id="home-graph-top-cuisine"),
                ],
                width=6,
            ),
        ],
        class_name="mt-4",
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
def update_home(df):
    df = pd.DataFrame.from_dict(df)

    number_of_countries = len(df[df["Country"].notna()]["Country"].unique())
    number_of_restaurants = len(df["Name"].unique())

    top_cuisine = df["Cuisine"].value_counts().index[0][0]
    top_cuisine_count = df["Cuisine"].value_counts().iloc[0]
    top_cuisine_formatted = f"{top_cuisine} ({top_cuisine_count} occurrences)"

    return number_of_countries, number_of_restaurants, top_cuisine_formatted


@callback(
    [
        Output("home-graph-top-countries", "figure"),
        Output("home-graph-top-cuisine", "figure"),
    ],
    Input("store", "data"),
)
def update_top_countries_graph(df):
    df = pd.DataFrame.from_dict(df)

    value_counts = df["Country"].value_counts()[:10].reset_index()
    fig1 = px.bar(value_counts, x="Country", y="count", labels={"count": "Number of restaurants"})

    value_counts = df["Cuisine"].value_counts()[:10].reset_index()
    fig2 = px.bar(value_counts, x="Cuisine", y="count", labels={"count": "Number of restaurants"})

    return fig1, fig2
