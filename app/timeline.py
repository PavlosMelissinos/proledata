import plotly.graph_objects as go
from datetime import datetime
import json
from app import definitions as defs

project_root = defs.project_root()


def parse_date(date_str):
    """Parse various date formats to datetime objects."""
    formats = [
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


def create_timeline(events):
    """Create an interactive timeline visualization from events."""

    # Define color mapping for event types
    color_map = {
        "diplomatic": "#74b9ff",
        "military": "#ff7675",
        "turkish_operation": "#a8e6cf",
        "civil_unrest": "#ffeaa7",
        "natural_disaster": "#fab1a0"
    }

    # Group events by historical context
    contexts = {}
    for event in events:
        context = event["historical_context"]
        if context not in contexts:
            contexts[context] = []
        contexts[context].append(event)

    # Create figure
    fig = go.Figure()

    # Calculate y positions for each context
    context_positions = {context: i for i, context in enumerate(contexts.keys())}

    # Add events to timeline
    for context, context_events in contexts.items():
        y_pos = context_positions[context]

        for event in context_events:
            start_date = parse_date(event["beginning_date"])
            end_date = parse_date(event["end_date"])

            # Get color based on event type (default to gray if not found)
            color = color_map.get(event["event_type"], "#636e72")

            # Add event marker
            fig.add_trace(go.Scatter(
                x=[start_date],
                y=[y_pos],
                mode="markers",
                marker=dict(
                    size=12,
                    color=color,
                    line=dict(width=1, color="black")
                ),
                name=event["title"],
                text=f"<b>{event['title']}</b><br>{event['summary']}",
                hoverinfo="text",
                showlegend=False
            ))

            # If event spans multiple days, add a line
            if start_date != end_date:
                fig.add_trace(go.Scatter(
                    x=[start_date, end_date],
                    y=[y_pos, y_pos],
                    mode="lines",
                    line=dict(color=color, width=4),
                    name=event["title"],
                    text=f"<b>{event['title']}</b><br>{event['summary']}",
                    hoverinfo="text",
                    showlegend=False
                ))

    # Add context labels on y-axis
    y_ticks = list(context_positions.values())
    y_labels = list(context_positions.keys())

    # Update layout
    fig.update_layout(
        title="Timeline of Events",
        showlegend=False,
        xaxis=dict(
            title="Date",
            type="date",
            showgrid=True
        ),
        yaxis=dict(
            title="Historical Context",
            ticktext=y_labels,
            tickvals=y_ticks,
            showgrid=True
        ),
        hovermode="closest",
        height=100 + (len(contexts) * 150),  # Dynamically adjust height
        plot_bgcolor="white"
    )

    # Add legend for event types
    legend_x = 1.02
    legend_y = 1
    for event_type, color in color_map.items():
        fig.add_trace(go.Scatter(
            x=[None],
            y=[None],
            mode="markers",
            marker=dict(size=10, color=color),
            name=event_type.replace("_", " ").title(),
            showlegend=True
        ))

    # Update layout for legend
    fig.update_layout(
        legend=dict(
            x=legend_x,
            y=legend_y,
            xanchor="left",
            yanchor="top",
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="black",
            borderwidth=1
        )
    )

    return fig


if __name__ == "__main__":
    events = json.loads((project_root / "resources" / "events.json").read_text())

    fig = create_timeline(events)
    fig.show()
