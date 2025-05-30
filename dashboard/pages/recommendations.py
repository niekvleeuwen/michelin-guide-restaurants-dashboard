import os

import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, State, callback, dcc, html

from dashboard.caching import retrieve_data
from dashboard.data.llm import LLM
from dashboard.utils import TITLE

PAGE_TITLE = "Recommendations"

dash.register_page(__name__, name=PAGE_TITLE, title=f"{PAGE_TITLE} | {TITLE}", order=2)


def layout():
    df = retrieve_data()
    return dbc.Container(
        [
            # Hero section
            dbc.Container(
                [
                    html.H1(PAGE_TITLE, className="text-primary"),
                    html.P(
                        "Get restaurants recommendations based on your preferences.",
                        className="lead",
                    ),
                ],
                className="py-4 text-center bg-light rounded-3 shadow-sm",
                fluid=True,
            ),
            dbc.Container(
                [
                    dbc.Alert(
                        """
                While the language model strives to provide accurate and helpful restaurant recommendations, it may
                occasionally produce incorrect or misleading information. Please verify any recommendations before
                making decisions based on them.
            """,
                        color="light",
                        className="my-3",
                    ),
                    dbc.Alert(
                        [
                            html.B("Note: "),
                            "Please provide an OpenAI API key in the .env file to use LLM functionality.",
                        ],
                        color="danger",
                    )
                    if not os.getenv("OPENAI_API_KEY")
                    else None,
                ]
            ),
            # Questions
            dbc.Container(
                dbc.Card(
                    [
                        dbc.CardHeader("Questions", className="bg-primary text-white"),
                        dbc.CardBody(
                            [
                                dbc.Form(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        dbc.Label("Location Preference"),
                                                        dcc.Dropdown(
                                                            options=construct_location_options(df),
                                                            id="location-preference",
                                                            placeholder="Enter city or country",
                                                        ),
                                                    ],
                                                    width=12,
                                                )
                                            ],
                                            className="mb-3",
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        dbc.Label("Cuisine Preference"),
                                                        dcc.Dropdown(
                                                            options=construct_cuisine_options(df),
                                                            id="cuisine-preference",
                                                            placeholder="Enter preferred cuisine",
                                                        ),
                                                    ],
                                                    width=12,
                                                )
                                            ],
                                            className="mb-3",
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        dbc.Label("Price Range"),
                                                        dbc.Checklist(
                                                            options=[
                                                                {
                                                                    "label": "Budget-Friendly",
                                                                    "value": "Budget-Friendly",
                                                                },
                                                                {"label": "Moderate", "value": "Moderate"},
                                                                {"label": "Premium", "value": "Premium"},
                                                                {"label": "Luxury", "value": "Luxury"},
                                                            ],
                                                            value=[
                                                                "Budget-Friendly",
                                                                "Moderate",
                                                                "Premium",
                                                                "Luxury",
                                                            ],
                                                            id="price-options",
                                                            inline=True,
                                                        ),
                                                    ],
                                                    width=12,
                                                )
                                            ],
                                            className="mb-3",
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        dbc.Label("Award"),
                                                        dbc.Checklist(
                                                            options=[
                                                                {
                                                                    "label": "Selected Restaurants",
                                                                    "value": "Selected Restaurants",
                                                                },
                                                                {"label": "Bib Gourmand", "value": "Bib Gourmand"},
                                                                {"label": "1 Star", "value": "1 Star"},
                                                                {"label": "2 Stars", "value": "2 Stars"},
                                                                {"label": "3 Stars", "value": "3 Stars"},
                                                            ],
                                                            value=[
                                                                "Selected Restaurants",
                                                                "Bib Gourmand",
                                                                "1 Star",
                                                                "2 Stars",
                                                                "3 Stars",
                                                            ],
                                                            id="award-options",
                                                            inline=True,
                                                            class_name="color-primary",
                                                        ),
                                                    ],
                                                    width=12,
                                                )
                                            ],
                                            className="mb-3",
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        dbc.Label(
                                                            "Describe what kind of restaurant you are looking for."
                                                        ),
                                                        dbc.Textarea(
                                                            id="recommendations-question-input",
                                                            placeholder="For example: restaurant with a set menu.",
                                                            style={"minHeight": "50px"},
                                                        ),
                                                    ],
                                                    width=12,
                                                )
                                            ],
                                            className="mb-3",
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        dbc.Button("Submit", id="submit-button", color="primary"),
                                                    ],
                                                    width="auto",
                                                )
                                            ]
                                        ),
                                    ]
                                )
                            ]
                        ),
                    ],
                    className="shadow-sm",
                ),
                className="my-3 p-1",
                fluid=True,
            ),
            # Recommended prompts section
            dbc.Container(
                dbc.Card(
                    [
                        dbc.CardHeader("Results", className="bg-secondary text-white"),
                        dbc.CardBody(
                            [
                                html.Div(id="recommendations-form-alert"),
                                html.Div("No results yet.", id="recommendations-form-output"),
                            ]
                        ),
                    ],
                    className="shadow-sm",
                ),
                className="my-3 p-1",
                fluid=True,
            ),
        ]
    )


def construct_location_options(df: pd.DataFrame) -> list[str]:
    locations = (
        df[df["Country"].notna()]["Country"].unique().tolist() + df[df["City"].notna()]["City"].unique().tolist()
    )
    return sorted(locations)


def construct_cuisine_options(df: pd.DataFrame) -> list[str]:
    cuisine_options = []
    cuisines = df[df["Cuisine"].notna()]["Cuisine"].unique().tolist()
    for cuisine in cuisines:
        cuisine_options += cuisine.split(", ")

    return sorted(list(set(cuisine_options)))


@callback(
    [
        Output("recommendations-form-output", "children"),
        Output("recommendations-form-alert", "children"),
    ],
    [
        Input("submit-button", "n_clicks"),
    ],
    [
        State("location-preference", "value"),
        State("cuisine-preference", "value"),
        State("price-options", "value"),
        State("award-options", "value"),
        State("recommendations-question-input", "value"),
    ],
    prevent_initial_call=True,
)
def process_form(
    n_clicks, location_preference, cuisine_preference, price_range, award_range, description_of_restaurant
):
    if not price_range:
        return [], dbc.Alert("Please select at least one price option.", color="danger")
    if not award_range:
        return [], dbc.Alert("Please select at least one award option.", color="danger")

    result = LLM().invoke_recommendations_llm(
        location_preference,
        cuisine_preference,
        price_range,
        award_range,
        description_of_restaurant,
    )
    return dcc.Markdown(result), []
