import plotly.express as px
from src.utils import value_counts_df     # helper we created

def generate_visualizations(df, splits):
    # ── 1. Treemap: Top Parental Guides ──────────────────────────
    guides = value_counts_df(df["parentalguide"], top_n=10, col_name="parentalguide")
    fig_treemap = px.treemap(
        guides,
        path=["parentalguide"],
        values="count",
        title="Top Parental Guides",
        color="count",
        color_continuous_scale="viridis",
    )
    fig_treemap.update_layout(template="plotly_dark", font=dict(color="yellow"))

    # ── 2. Bar: Top Genres ───────────────────────────────────────
    genres = value_counts_df(splits["genre"]["genre"], col_name="genre")
    fig_bar_language = px.bar(
        genres,
        x="count",
        y="genre",
        orientation="h",
        color="count",
        text="percentage",
        title="Top Genres",
        color_continuous_scale="viridis",
    )
    fig_bar_language.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
    fig_bar_language.update_layout(
        template="plotly_dark",
        font=dict(color="yellow"),
        yaxis=dict(categoryorder="total ascending"),
    )

    # ── 3. Choropleth: Producing Countries ───────────────────────
    countries = value_counts_df(splits["country"]["country"], top_n=30, col_name="country")

    country_mapping = {
        "United States": "USA",  "United Kingdom": "GBR", "France": "FRA",
        "Germany": "DEU",        "Japan": "JPN",          "India": "IND",
        "Australia": "AUS",      "Canada": "CAN",         "China": "CHN",
        "Italy": "ITA",          "Spain": "ESP",          "Mexico": "MEX",
        "Hong Kong": "HKG",      "Sweden": "SWE",         "Denmark": "DNK",
        "New Zealand": "NZL",    "Belgium": "BEL",        "South Korea": "KOR",
        "Ireland": "IRL",        "Netherlands": "NLD",    "South Africa": "ZAF",
        "Norway": "NOR",         "Austria": "AUT",        "Turkey": "TUR",
        "West Germany": "DEU",   "Switzerland": "CHE",
    }
    countries["country_iso"] = countries["country"].map(country_mapping)

    fig_choropleth = px.choropleth(
        countries,
        locations="country_iso",
        hover_name="country",
        color="count",
        title="Top Producing Countries",
        projection="natural earth",
        color_continuous_scale="viridis",
    )
    fig_choropleth.update_layout(template="plotly_dark", font=dict(color="yellow"))

    # ── 4. Box Plot: Ratings Distribution ────────────────────────
    fig_boxplot = px.box(
        df,
        x="rating",
        title="Ratings Distribution",
    )
    fig_boxplot.update_traces(marker=dict(color="yellow"))
    fig_boxplot.update_layout(template="plotly_dark", font=dict(color="yellow"))

    return fig_treemap, fig_bar_language, fig_choropleth, fig_boxplot
