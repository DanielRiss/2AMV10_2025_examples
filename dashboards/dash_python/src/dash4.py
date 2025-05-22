import plotly.express as px

def generate_visualizations(df, splits=None):
    # ── Line 1: works per year ────────────────────────────────
    yearly_counts = (
        df.groupby("year")
        .size()
        .reset_index(name="count")
    )
    fig_count = px.line(
        yearly_counts,
        x="year",
        y="count",
        title="Work Count Over Time",
    )

    # ── Line 2: mean votes per year ───────────────────────────
    yearly_votes = (
        df.groupby("year")["votes"]
        .mean()
        .reset_index(name="votes")
    )
    fig_votes = px.line(
        yearly_votes,
        x="year",
        y="votes",
        title="Work Votes Over Time",
    )

    # Shared dark theme + yellow line
    for fig in (fig_count, fig_votes):
        fig.update_traces(line=dict(color="yellow"))
        fig.update_layout(template="plotly_dark", font=dict(color="yellow"))

    return fig_count, fig_votes
