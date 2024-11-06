import os
from datetime import datetime

import dash
import dash_bootstrap_components as dbc
from dash import ALL, Input, Output, State, callback, dcc, html
from data.llm import LLM
from loguru import logger
from utils import TITLE

PAGE_TITLE = "LLM Analysis"
RECOMMENDED_PROMPTS = [
    "How many 3-star restaurants are there in France?",
    "What is the most popular cuisine for 3-star restaurants?",
    "List the most affordable Michelin-star restaurants in Rotterdam.",
]


dash.register_page(__name__, name=PAGE_TITLE, title=f"{PAGE_TITLE} | {TITLE}", order=3)

layout = dbc.Container(
    [
        # Hero section
        dbc.Container(
            [
                html.H1("LLM Analysis", className="display-4 text-primary"),
                html.P(
                    "Explore the data interactively through natural language prompts.",
                    className="lead",
                ),
                dbc.Textarea(
                    id="analysis-question-input",
                    placeholder="Enter any question related to Michelin data...",
                    style={"minHeight": "50px"},
                    class_name="mt-3",
                ),
                dbc.Button("Submit", color="primary", id="analysis-submit-button", className="mt-2"),
            ],
            className="py-4 text-center bg-light rounded-3 shadow-sm",
            fluid=True,
        ),
        dbc.Container(
            [
                dbc.Alert(
                    """
                While the language model strives to provide accurate and helpful answers, it may
                occasionally produce incorrect or misleading information. Please verify any important information.
            """,
                    color="light",
                    className="my-3",
                ),
                dbc.Alert(
                    [html.B("Note: "), "Please provide an OpenAI API key in the .env file to use LLM functionality."],
                    color="danger",
                )
                if not os.getenv("OPENAI_API_KEY")
                else None,
            ]
        ),
        # Recommended prompts section
        dbc.Container(
            dbc.Card(
                [
                    dbc.CardHeader("Recommended Prompts", className="bg-secondary text-white"),
                    dbc.ListGroup(
                        [
                            dbc.ListGroupItem(
                                prompt, action=True, id={"type": "analysis-recommended-prompt", "index": i}
                            )
                            for i, prompt in enumerate(RECOMMENDED_PROMPTS)
                        ],
                        flush=True,
                    ),
                ],
                className="shadow-sm",
            ),
            className="my-3 p-1",
            fluid=True,
        ),
        # Result card to display the answer
        dbc.Container(
            dbc.Card(
                [
                    dbc.CardHeader("Result", className="bg-primary text-white"),
                    dbc.CardBody(
                        [
                            dbc.Spinner(id="analysis-result-output", children="-", color="primary", delay_show=100),
                        ]
                    ),
                ],
                style={"minHeight": "150px"},
                className="shadow-sm",
            ),
            className="my-3 p-1",
            fluid=True,
        ),
        # History section
        dbc.Container(
            dbc.Card(
                [
                    dbc.CardHeader("Prompt History", className="bg-info text-white"),
                    dbc.CardBody(
                        [
                            dbc.Table(
                                [
                                    html.Thead(
                                        html.Tr(
                                            [
                                                html.Th("Time"),
                                                html.Th("Question"),
                                                html.Th("Answer"),
                                            ]
                                        )
                                    ),
                                    html.Tr(html.Td("No questions asked yet."), id="analysis-history-list-placeholder"),
                                ],
                                id="analysis-history-list",
                            )
                        ]
                    ),
                ],
                className="shadow-sm",
            ),
            className="my-3 p-1",
            fluid=True,
        ),
    ],
    fluid=True,
)


@callback(
    [
        Output("analysis-result-output", "children"),
        Output("analysis-history-list", "children"),
        Output("analysis-history-list-placeholder", "children"),
    ],
    [
        Input("analysis-submit-button", "n_clicks"),
        Input({"type": "analysis-recommended-prompt", "index": ALL}, "n_clicks"),
    ],
    [
        State("analysis-question-input", "value"),
        State("analysis-history-list", "children"),
    ],
    prevent_initial_call=True,
)
def update_result(_, __, user_question, history_list):
    """Update results for the LLM analysis page."""
    trigger = dash.callback_context.triggered_id

    if isinstance(trigger, dict) and trigger["type"] == "analysis-recommended-prompt":
        prompt = RECOMMENDED_PROMPTS[trigger["index"]]
        logger.debug(f"Recommended prompt {prompt}")
    elif trigger == "analysis-submit-button":
        prompt = user_question
        logger.debug(f"User prompt {prompt}")
    else:
        raise ValueError(f"Incorrect trigger: {trigger}")

    if not prompt:
        return "Please provide a question.", dash.no_update, dash.no_update

    result = LLM().invoke_analysis_llm(prompt)

    result = dcc.Markdown(result)

    # Add to history
    new_history = html.Tr([html.Td(datetime.now().strftime("%H:%M:%S")), html.Td(prompt), html.Td(result)])
    history_list = (history_list or []) + [new_history]

    return result, history_list, []


@callback(
    Output("analysis-question-input", "value"),
    Input({"type": "analysis-recommended-prompt", "index": ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def fill_question_input(_):
    """To improve UX, add the recommended question to the input field."""
    trigger = dash.callback_context.triggered_id
    return RECOMMENDED_PROMPTS[trigger["index"]]
