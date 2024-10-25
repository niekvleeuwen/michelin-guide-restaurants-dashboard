import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, html
from dash.exceptions import PreventUpdate

from dashboard.utils import TITLE

PAGE_TITLE = "Recommendations"

dash.register_page(__name__, name=PAGE_TITLE, title=f"{PAGE_TITLE} | {TITLE}", order=2)

layout = [
    html.H3("Recommendations", className="mb-3"),
    html.P(
        """This page makes restaurant recommendations using an LLM.
        """
    ),
    dbc.Row(
        dbc.Col(
            dbc.Form(
                [
                    dbc.Label("Question", html_for="recommendations-prompt"),
                    dbc.Textarea(
                        id="recommendations-prompt",
                        placeholder="""Please enter prompt.""",
                    ),
                    dbc.Button(
                        "Get a recommendation",
                        id="recommendations-submit-btn",
                        class_name="mt-2",
                    ),
                ]
            ),
            width=6,
        )
    ),
    dbc.Row(
        dbc.Col([html.H5("Recommendation:"), html.P("-", id="recommendations-output")]),
        class_name="mt-5",
    ),
]


@callback(
    Output("recommendations-output", "children"),
    Input("recommendations-submit-btn", "n_clicks"),
    State("recommendations-prompt", "value"),
)
def recommendations_submit(n_clicks, prompt: str) -> str:
    if not n_clicks:
        raise PreventUpdate

    # Ask LLM here

    return prompt
