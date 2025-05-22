import plotly.express as px

def generate_visualizations(series, splits=None):
    # ── Bar 1: average votes per parental guide ──
    df_mean = (
        series.groupby("parentalguide")["votes"]
        .mean()
        .reset_index(name="votes")
        .sort_values("votes", ascending=False)
    )
    fig_bar_mean_votes = px.bar(
        df_mean,
        x="parentalguide",
        y="votes",
        title="Parental Guide by Mean Votes",
        color="votes",
    )

    # ── Bar 2: total count per parental guide ──
    df_count = (
        series.groupby("parentalguide")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )
    fig_bar_count = px.bar(
        df_count,
        x="parentalguide",
        y="count",
        title="Parental Guide by Count",
        color="count",
    )

    # consistent dark theme styling
    for fig in (fig_bar_mean_votes, fig_bar_count):
        fig.update_layout(template="plotly_dark", font=dict(color="yellow"))

    return fig_bar_mean_votes, fig_bar_count
