import plotly.express as px
from src.utils import value_counts_df

def generate_visualizations(df, splits):
    # ── 1. Donut: Top Creators ───────────────────────────────────
    creators = value_counts_df(splits["creators"]["creators"], top_n=3, col_name="creators")
    fig_donut = px.pie(
        creators,
        names="creators",
        values="count",
        title="Top Creators",
        hole=0.5
    )
    fig_donut.update_layout(template="plotly_dark", font=dict(color="yellow"))

    # ── 2. Bar (h): Production Companies ────────────────────────
    prod = value_counts_df(splits["production_company"]["production_company"],
                           top_n=10, col_name="production_company")
    fig_prod = px.bar(
        prod,
        x="count",
        y="production_company",
        orientation="h",
        color="count",
        text="percentage",
        title="Top Production Companies",
        color_continuous_scale="viridis",
    )
    fig_prod.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
    fig_prod.update_layout(
        template="plotly_dark",
        font=dict(color="yellow"),
        yaxis=dict(categoryorder="total ascending"),
    )

    # ── 3. Bar (v): Stars ───────────────────────────────────────
    stars = value_counts_df(splits["stars"]["stars"], top_n=10, col_name="stars")
    fig_stars = px.bar(
        stars,
        x="stars",
        y="count",
        orientation="v",
        color="count",
        text="percentage",
        title="Top Stars",
        color_continuous_scale="viridis",
    )
    fig_stars.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
    fig_stars.update_layout(template="plotly_dark", font=dict(color="yellow"))

    # ── 4. Bar (v): Languages ───────────────────────────────────
    langs = value_counts_df(splits["language"]["language"], top_n=10, col_name="language")
    fig_lang = px.bar(
        langs,
        x="language",
        y="count",
        orientation="v",
        color="count",
        text="percentage",
        title="Top Languages",
        color_continuous_scale="viridis",
    )
    fig_lang.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
    fig_lang.update_layout(template="plotly_dark", font=dict(color="yellow"))

    return fig_donut, fig_prod, fig_stars, fig_lang
