import plotly.graph_objects as go

from utils import MICHELIN_PRIMARY_COLOR


def default_layout() -> dict:
    """Return a Plotly Graph layout to be used as default."""
    return go.Layout(
        margin=dict(
            t=30,  # Extra space to accommodate the Plotly utility bar
            b=10,
            l=10,
            r=10,
        ),
        font_family="Figtree",
    )


def apply_style_to_fig(fig: go.Figure, apply_trace_color: bool = True) -> go.Figure:
    """Apply the default style to a figure.

    Args:
        apply_trace_color (bool): if True, the Michelin primary color will be used for the plot.
    """
    # Apply layout
    layout = default_layout()
    fig.update_layout(layout)

    if apply_trace_color:
        fig.update_traces(marker_color=MICHELIN_PRIMARY_COLOR)

    return fig
