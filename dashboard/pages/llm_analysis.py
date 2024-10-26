import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, dcc, html
from dash.exceptions import PreventUpdate

from dashboard.data.llm import LLM
from dashboard.utils import TITLE

PAGE_TITLE = "LLM Analysis"

dash.register_page(__name__, name=PAGE_TITLE, title=f"{PAGE_TITLE} | {TITLE}", order=3)

layout = [
    html.H3("LLM Analysis", className="mb-3"),
    html.P(
        """The LLM Analysis page allows users to explore the data interactively through natural language prompts.
        """
    ),
    # TODO add example queries
    # 1. How many restaurants are there when filtering for country France?
    # 2. Show all three-star restaurants in France
    # 3. What are the most common cuisines in Japan?
    dbc.Row(
        dbc.Col(
            dbc.Form(
                [
                    dbc.Label("Question", html_for="analysis-prompt"),
                    dbc.Textarea(id="analysis-prompt", placeholder="""Enter any question related to Michelin data"""),
                    dbc.Button("Execute", id="analysis-submit-btn", class_name="mt-2"),
                ]
            ),
            width=6,
        )
    ),
    dbc.Row(dbc.Col([dbc.Spinner([html.H5("Result:"), html.Div("-", id="analysis-output")])]), class_name="mt-5"),
]


@callback(
    Output("analysis-output", "children"), Input("analysis-submit-btn", "n_clicks"), State("analysis-prompt", "value")
)
def analysis_submit(n_clicks, prompt: str) -> str:
    if not n_clicks:
        raise PreventUpdate

    result = LLM().invoke_llm(prompt)

    return dcc.Markdown(result)
