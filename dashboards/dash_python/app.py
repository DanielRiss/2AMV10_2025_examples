from pathlib import Path

import dash_bootstrap_components as dbc
import pandas as pd
from dash import Dash, dcc, html, Input, Output  # State not currently needed

from src.const import get_constants
from src import dash1, dash2, dash3, dash4

# ──────────────────────────────────────────────────────────────────────────────
# Data & constants
# ──────────────────────────────────────────────────────────────────────────────
DATA_DIR = Path("dashboards/dash_python/data")

MOVIES = pd.read_csv(DATA_DIR / "movie_after_cleaning.csv")
MOVIES_SPLITS = pd.read_excel(DATA_DIR / "splits_movie.xlsx", sheet_name=None)
SERIES = pd.read_csv(DATA_DIR / "series_after_cleaning.csv")
SERIES_SPLITS = pd.read_excel(DATA_DIR / "splits_series.xlsx", sheet_name=None)

DATA_BY_TAB = {
    "movie": (MOVIES, MOVIES_SPLITS),
    "series": (SERIES, SERIES_SPLITS),
}

VISUALIZATION_BUILDERS = {
    "overview": (dash1.generate_visualizations, 4),
    "content_creators": (dash2.generate_visualizations, 4),
    "parental": (dash3.generate_visualizations, 2),
    "year": (dash4.generate_visualizations, 2),
}

# Top-level stats
NUM_WORKS, NUM_COUNTRIES, NUM_LANGUAGES, AVG_VOTES = get_constants(
    MOVIES, SERIES, MOVIES_SPLITS, SERIES_SPLITS
)

MAX_OPTIONS_DISPLAY = 3_300
DROPDOWN_OPTIONS = {
    "movie": [{"label": t, "value": t} for t in MOVIES["title"][:MAX_OPTIONS_DISPLAY]],
    "series": [{"label": t, "value": t} for t in SERIES["title"][:MAX_OPTIONS_DISPLAY]],
}

BRAND_COLOR = "#deb522"

CARD_STYLE = {
    "paddingBlock": "10px",
    "backgroundColor": BRAND_COLOR,
    "border": "none",
    "borderRadius": "10px",
}

TAB_STYLE_IDLE = {
    "borderRadius": "10px",
    "padding": 0,
    "marginInline": "5px",
    "display": "flex",
    "alignItems": "center",
    "justifyContent": "center",
    "fontWeight": "bold",
    "backgroundColor": BRAND_COLOR,
    "border": "none",
}
TAB_STYLE_ACTIVE = {**TAB_STYLE_IDLE, "textDecoration": "underline"}

# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────
def stats_card(title: str, value, img: str) -> html.Div:
    """Single KPI card."""
    return html.Div(
        dbc.Card(
            [
                dbc.CardImg(src=img, top=True, style={"width": "50px", "alignSelf": "center"}),
                dbc.CardBody(
                    [
                        html.P(value, style={"margin": 0, "fontSize": "22px", "fontWeight": "bold"}),
                        html.H4(title, style={"margin": 0, "fontSize": "18px", "fontWeight": "bold"}),
                    ],
                    style={"textAlign": "center"},
                ),
            ],
            style=CARD_STYLE,
        )
    )


def wrap_figures(figures) -> html.Div:
    """Lay out a list of Plotly figures in a 2-column grid."""
    return html.Div(
        [
            html.Div(dcc.Graph(figure=fig), style={"width": "50%", "display": "inline-block"})
            for fig in figures
        ]
    )


# ──────────────────────────────────────────────────────────────────────────────
# Dash app
# ──────────────────────────────────────────────────────────────────────────────
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], title="IMDB Data Analysis Dashboard")

app.layout = html.Div(
    [
        dbc.Container(
            [
                # ── Header with nav tabs ──────────────────────────────────
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="./assets/imdb.png", width=150), width=2),
                        dbc.Col(
                            dcc.Tabs(
                                id="graph-tabs",
                                value="overview",
                                children=[
                                    dcc.Tab(label="Overview", value="overview", style=TAB_STYLE_IDLE, selected_style=TAB_STYLE_ACTIVE),
                                    dcc.Tab(label="Content creators", value="content_creators", style=TAB_STYLE_IDLE, selected_style=TAB_STYLE_ACTIVE),
                                    dcc.Tab(label="Parental Guide", value="parental", style=TAB_STYLE_IDLE, selected_style=TAB_STYLE_ACTIVE),
                                    dcc.Tab(label="Year", value="year", style=TAB_STYLE_IDLE, selected_style=TAB_STYLE_ACTIVE),
                                ],
                                style={"marginTop": "15px", "width": "600px", "height": "50px"},
                            ),
                            width=6,
                        ),
                    ]
                ),
                # ── KPI cards ─────────────────────────────────────────────
                dbc.Row(
                    [
                        dbc.Col(stats_card("Work", NUM_WORKS, "./assets/movie-icon.png"), width=3),
                        dbc.Col(stats_card("Language", NUM_LANGUAGES, "./assets/language-icon.svg"), width=3),
                        dbc.Col(stats_card("Country", NUM_COUNTRIES, "./assets/country-icon.png"), width=3),
                        dbc.Col(stats_card("Average Votes", AVG_VOTES, "./assets/vote-icon.png"), width=3),
                    ],
                    style={"marginBlock": "10px"},
                ),
                # ── Movie / Series selector ───────────────────────────────
                dbc.Row(
                    dcc.Tabs(
                        id="data-tabs",
                        value="movie",
                        children=[
                            dcc.Tab(label="Movie", value="movie",
                                    style={"border": "1px solid white", "backgroundColor": "black", "color": BRAND_COLOR, "fontWeight": "bold"},
                                    selected_style={"border": "1px solid white", "backgroundColor": "black", "color": BRAND_COLOR, "fontWeight": "bold", "textDecoration": "underline"}),
                            dcc.Tab(label="Series", value="series",
                                    style={"border": "1px solid white", "backgroundColor": "black", "color": BRAND_COLOR, "fontWeight": "bold"},
                                    selected_style={"border": "1px solid white", "backgroundColor": "black", "color": BRAND_COLOR, "fontWeight": "bold", "textDecoration": "underline"}),
                        ],
                        style={"padding": 0},
                    )
                ),
                # ── Dynamic figures ───────────────────────────────────────
                dbc.Row(
                    dcc.Loading(html.Div(id="tabs-content"), type="default", color=BRAND_COLOR)
                ),
            ],
            style={"padding": 0},
        )
    ],
    style={"backgroundColor": "black", "minHeight": "100vh"},
)

# ──────────────────────────────────────────────────────────────────────────────
# Callbacks
# ──────────────────────────────────────────────────────────────────────────────
@app.callback(Output("tabs-content", "children"), Input("graph-tabs", "value"), Input("data-tabs", "value"))
def update_tab(graph_tab: str, data_tab: str):
    """Render the correct set of figures based on tab selections."""
    data, splits = DATA_BY_TAB[data_tab]
    builder, expected_figs = VISUALIZATION_BUILDERS[graph_tab]

    figures = builder(data, splits)
    if len(figures) != expected_figs:
        raise ValueError(f"{builder.__name__} returned {len(figures)} figures (expected {expected_figs}).")

    return wrap_figures(figures)


if __name__ == "__main__":
    app.run_server(debug=False)
