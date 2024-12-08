import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Constants
COLORS = {
    'spending': ['#82ca9d', '#8884d8'],
    'departures': '#ff8042',
    'hirings': '#82ca9d',
    'cumulative': 'red',
    'budget': '#8884d8',
    'reference': 'red'
}
BAR_WIDTH = 0.3


def spending_traces(labels: list[str], values: list[float]) -> list[go.Bar]:
    """Creates spending visualization traces"""
    return [
        go.Pie(
            title="Συνολικές Δαπάνες Υγείας 2022",
            labels = labels,
            values = values,
            legend='legend3',
        )
    ]


def personnel_traces(x, y) -> list[go.Waterfall | go.Scatter]:
    """Creates personnel waterfall chart"""
    y_cumulative = [sum(y[:i+1]) for i in range(len(y))]
    return [
        go.Waterfall(
            name="Μεταβολή Προσωπικού",
            orientation="v",
            measure=["relative", "relative", "relative", "relative", "relative"],
            x=x,
            y=y,
            xaxis='x1',
            yaxis='y1',
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            decreasing={"marker": {"color": "#ff2022"}},
            increasing={"marker": {"color": "#82ca9d"}},
            totals={"marker": {"color": "grey"}},
            textposition="outside",
            legend='legend1',
        ),
        go.Scatter(
            name='Σωρευτική Μεταβολή',
            x=x,
            y=y_cumulative,
            xaxis='x1',
            yaxis='y1',
            mode='lines+markers',
            line={"color": "black", "width": 1},
            legend='legend1',
        )
    ]


def budget_traces(
    labels: list[str],
    values: list[int]
) -> list[go.Bar | go.Scatter]:
    """Creates budget visualization traces"""
    return [
        go.Bar(
            name='Προϋπολογισμός',
            x=labels,
            y=values,
            xaxis='x2',
            yaxis='y2',
            width=BAR_WIDTH,
            marker_color=COLORS['budget'],
            legend='legend2',
        ),
        go.Scatter(
            name='Επίπεδο 2024',
            x=labels,
            y=values[0:1] * 3,
            xaxis='x2',
            yaxis='y2',
            mode='lines',
            line={"color": COLORS['reference'], "dash": 'dash'},
            legend='legend2',
        )
    ]


def add_traces(fig: go.Figure, traces: list[go.Bar | go.Scatter], row: int, col: int) -> None:
    """Adds traces to a specific subplot"""
    for trace in traces:
        fig.add_trace(trace, row=row, col=col)


def create_figure(titles) -> go.Figure:
    """Creates the base figure with subplots"""
    return make_subplots(
        rows=3,
        cols=1,
        subplot_titles=titles,
        vertical_spacing=0.2,
    )


def apply_layout(fig: go.Figure) -> None:
    """Applies common layout settings"""
    fig.update_layout(
        barmode='stack',
        showlegend=True,
        plot_bgcolor='white',
        title_x=0.5,
        margin={"l": 50, "r": 50, "t": 100, "b": 50},
        width=1000
    )
    fig.add_hline(y=0, line_width=1, line_color="black", row=2, col=1)
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')


def create_healthcare_plots() -> go.Figure:
    """Creates complete healthcare visualization"""
    spending_data = {
        "labels": ['Κρατική Δαπάνη', 'Ιδιωτικές Πληρωμές & Ασφαλιστικά'],
        "values": [30.2, 69.8],
    }
    personnel_data = {
        "x": ["2022", "Αποχωρήσεις 2023-2024", "Προσλήψεις 2023-2024",
              "Αποχωρήσεις 2025", "Προσλήψεις 2025"],
        "y": [0, -5840, 4070, -2701, 3440],
    }
    budget_data = {
        "labels": ['2024', '2025 (Φαινομενικό)', '2025 (Πραγματικό)'],
        "values": [6050, 6600, 5662],
    }

    titles = [
        'Κατανομή Δαπανών Υγείας',
        'Μεταβολή Προσωπικού',
        'Εξέλιξη Προϋπολογισμού (σε εκατ. €)'
    ]

    # Create traces
    spending = spending_traces(**spending_data)
    personnel = personnel_traces(**personnel_data)
    budget = budget_traces(**budget_data)

    layout = go.Layout(
        **{
            "title": {"text": "Προϋπολογισμός Υγείας"},
            "grid": {"rows": 3, "columns": 1, "pattern": "independent"},
            "yaxis3": {"domain": [0.75, 1], "anchor": "y3"},
            "yaxis1": {"domain": [0.35, 0.6], "anchor": "y1"},
            "yaxis2": {"domain": [0, 0.25], "anchor": "y2"},
            "legend3": {
                "title": {
                    "text": "Κατανομή Δαπανών Υγείας",
                },
                "y": 0.85,
                "bgcolor": "Orange",
            },
            "legend1": {
                "title": {
                    "text": "Μεταβολή προσωπικού",
                },
                "y": 0.50,
                "bgcolor": "Orange",
            },
            "legend2": {
                "title": {
                    "text": "Εξέλιξη Προϋπολογισμού (σε εκατ. €)",
                },
                "y": 0.20,
                "bgcolor": "Orange",
            },
        }
    )
    return go.Figure(
        data=spending + personnel + budget,
        layout=layout,
    )


if __name__ == "__main__":
    fig = create_healthcare_plots()
    fig.show()
    # fig.write_html("healthcare_plots.html")

    import os

    if not os.path.exists("docs"):
        os.mkdir("docs")

    fig.write_html("docs/health.html")
