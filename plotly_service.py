import plotly.graph_objects as go


def cv_percent_graph(value):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            title={"text": "CV Match %"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#63f542"},
                "steps": [
                    {"range": [0, 50], "color": "#f56342"},
                    {"range": [50, 75], "color": "#ecf542"},
                    {"range": [75, 100], "color": "green"},
                ],
                "threshold": {
                    "line": {"color": "black", "width": 4},
                    "thickness": 0.75,
                    "value": value,
                },
            },
        )
    )

    return fig
