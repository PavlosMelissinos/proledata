from datetime import datetime
import plotly.graph_objects as go
from app import definitions as defs
import textwrap

project_root = defs.project_root()

# Color mapping
color_map = {
    "diplomatic": "#74b9ff",
    "military": "#ff7675",
    "turkish_operation": "#a8e6cf",
    "civil_unrest": "#ffeaa7",
    "natural_disaster": "#fab1a0"
}

def wrap_text(text: str, width: int = 60) -> str:
    """
    Wraps text by inserting <br> tags every `width` characters.
    For example tooltips.

    Args:
        text (str): The tooltip text to wrap
        width (int): Maximum number of characters before inserting a line break

    Returns:
        str: The wrapped text with <br> tags inserted
    """

    return "<br>".join(textwrap.wrap(text, width=width))


def parse_date(date_str):
    """Parse various date formats to datetime objects."""
    formats = [
        "%Y-%m-%dT%H:%M:%S",  # 2024-12-08T12:00:00
        "%Y-%m-%d",  # 2024-12-08
        "%Y-%m",     # 2024-12
        "%Y"         # 2024
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Date {date_str} is not in any of the expected formats")


def hover_text(title, date, summary, historical_context, **context):
    wrap_length = context.get("wrap_length", 60)
    summary_wrapped = wrap_text(summary, wrap_length)
    historical_context_wrapped = wrap_text(historical_context, wrap_length)
    return f"<b>{title}</b><br>Ημερομηνία: {date}<br>{historical_context_wrapped}<br><br>{summary_wrapped}<br>"


def text(title, date, **_):
    d = parse_date(date)
    year = d.year
    # month = parse_date(date).month
    month_to_greek = {
        "January": "Ιανουάριος",
        "February": "Φεβρουάριος",
        "March": "Μάρτιος",
        "April": "Απρίλιος",
        "May": "Μάιος",
        "June": "Ιούνιος",
        "July": "Ιούλιος",
        "August": "Αύγουστος",
        "September": "Σεπτέμβριος",
        "October": "Οκτώβριος",
        "November": "Νοέμβριος",
        "December": "Δεκέμβριος",
    }
    month = month_to_greek[d.strftime("%B")]
    return f"{year} - {month}<br><b>{title}</b>"


def create_timeline_trace(name, events, vertical=False, scale=1.0):
    fig = go.Figure()
    events = events[::-1] if vertical else events

    x = [0] * len(events) if vertical else list(range(len(events)))
    y = list(range(len(events))) if vertical else [0] * len(events)

    color = lambda event: color_map.get(event["event_type"], "#636e72")

    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode="lines",
        line=dict(color="#2d3436", width=3),
        #name=name,
        text=[],
        textposition="bottom center",
        showlegend=False,
    ))

    # Add event marker on the central line
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode="markers",
        marker=dict(
            size=16,
            color=[color(e) for e in events],
            line=dict(width=1, color="black")
        ),
        showlegend=False,
        #hoverinfo="skip"
    ))

    for i, event in enumerate(events):
        txt = text(**event)
        text_side = -1 if i%2==0 else 1
        fig.add_annotation(
            text=txt,
            align="center",
            # showarrow=False,
            ax=0.1 * text_side if vertical else i + 0.05,
            ay=i if vertical else 0.05,
            axref="x",
            ayref="y",
            xref="x",
            yref="y",
            x=0.004 * text_side if vertical else i,
            y=i if vertical else 0,
            bgcolor=color(event),
            borderwidth=1,
            borderpad=10,
            #arrowhead=1,
            hovertext=hover_text(**event),
            #hoverfont=dict(size=16),
        )

    smart_margin = lambda n1, n2: max(0.5, (n1 - n2) * 0.2 * (1 if n1 > n2 else -1))
    mx = smart_margin(x[0], x[-1])
    my = smart_margin(y[0], y[-1])

    print(y[-1])
    fig.update_layout(
        title={
            "text": name,
            "font": {"size": 36},
            #"automargin": True,
            "y": 0.88,
            "yref": "container",
        },
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[y[0] - my, y[-1] + my]
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[x[0] - mx, x[-1] + mx]
        ),
        font=dict(
            family="Courier New, monospace",
            size=16,
            #color="RebeccaPurple"
        ),
        hoverlabel=dict(
            # bgcolor="white",
            font_size=18,
            font_family="Rockwell"
        )
    )

    return fig


if __name__ == "__main__":
    events = json.loads((project_root / "resources" / "events.json").read_text())

    vertical = True
    fig = create_timeline_trace(
        name="Ιστορικό του πολέμου στη Συρία",
        events=events,
        vertical=vertical
    )
    fig.show()

    static_path = project_root / "static"
    if not static_path.exists():
        static_path.mkdir()

    fig.write_html(static_path / "syria_war.html")
