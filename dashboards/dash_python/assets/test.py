import nbformat as nbf

canvas_text = '''# 01 – Layout & Structure

*Insanely detailed deep‑dive into the skeleton of the IMDB Dash dashboard*

---

## 0 ▪︎ Notebook Goals

**After completing this notebook you will be able to**

1. Explain *why* we paired **Dash** with **Bootstrap** and how their responsibilities differ.
2. Re‑build the full page layout—from logo to loading spinner—*from scratch* in ≤ 60 loc.
3. Audit any new component for visual and responsive consistency (12‑column grid, dark theme, brand yellow).
4. Extend the layout with zero global side‑effects (encapsulation & helper functions).

> 💡 **Prerequisites**  – Python 3.10+, basic Plotly, run `conda activate imdb-dash` then `pip install -r requirements.txt`.

---

## 0 a ▪︎ Dashboard Purpose & Component Map

This section gives you the **30‑second elevator pitch** for the dashboard *and* shows how every moving part is wired together.

### What the Dashboard Does

* **Exploratory analytics** for \~180 K films & series scraped from IMDB after heavy cleaning.
* Surfaces **four KPI cards** (works, languages, countries, avg votes) for an at‑a‑glance health check.
* Offers **8 visual analysis views** (4 graph‑tabs × 2 data‑tabs) covering global trends, content‑creator stats, parental‑rating breakdowns, and year‑over‑year patterns.
* Stays **interactive** — every tab click triggers a single callback that fetches just the needed data & figures (zero redundant rendering).

### How the Components Connect

This dashboard responds dynamically to tab selection by using a single callback function that connects the **tab UI**, **data loaders**, and **visualisation builders**. Here's how that flow works in practice:

1. **User selects tabs** – The dashboard has two tab sets: `graph-tabs` (which analysis view to show) and `data-tabs` (whether to use Movie or Series data). These serve as inputs to the central callback.

2. **Callback receives tab values** – The `@app.callback` decorator in `app.py` listens for changes to these tabs. It sends the selected values into the `update_tab()` function.

3. **Data is loaded** – The `load_data(tab)` helper selects the correct `.csv` and `.xlsx` combo based on whether the user is exploring movies or series.

4. **Builder function is selected** – Depending on the analysis tab (`overview`, `content_creators`, etc.), the callback looks up the appropriate visualisation generator (like `generate_visualizations1`). This lookup happens via a dictionary (`VISUALIZATION_BUILDERS`), making the logic declarative and easy to extend.

5. **Figures are generated** – The selected builder function is run with the loaded data, returning a fixed number of Plotly figures (2 or 4 depending on the tab).

6. **Figures are wrapped into layout** – These figures are passed into `wrap_figures()`, a helper that arranges them into a 2-column grid using `dcc.Graph` components.

7. **Dash injects the layout** – The wrapped layout is returned as the output of the callback, replacing the contents of `<div id='tabs-content'>` in the app layout.

This pattern is powerful because it decouples content generation from layout logic, and avoids repetitive if-else blocks. Adding a new tab requires only adding a new builder function and registering it in a dictionary—no need to rewrite the callback itself.

```mermaid
erDiagram
    DataFrame ||--o{ VisualizationBuilder : "feeds"
    VisualizationBuilder ||--o{ Figure : "returns"
    Figure ||--o{ wrap_figures : "arranged into"
    Tabs }o--o{ Callback : "updates"
```

```mermaid
flowchart LR
  subgraph UI
    A[graph‑tabs] --select--> CB[Dash Callback]
    B[data‑tabs]  --select--> CB
  end
  CB --"load_data(tab)"--> DF[(Pandas DataFrames)]
  CB --"builder(tab)"--> FG{{Plotly Figures}}
  FG --"wrap_figures"--> LC[<div id='tabs‑content'>]
  LC --> Page[Browser]

  style CB fill:#222,color:#fff
  style FG fill:#444,color:#fff
```

* **`load_data(tab)`** returns the right pair of *data* and *splits* DataFrames.
* **`VISUALIZATION_BUILDERS`** dict maps the selected graph‑tab → generator function (`dash1`…`dash4`).
* **`wrap_figures`** lays out the resulting Plotly figures in a responsive 2‑column grid.

> 🛠 **Extension hint:** adding a new analysis tab is a 3‑step workflow: `generate_visualizationsX`, register in `VISUALIZATION_BUILDERS`, add a UI tab label—no extra callbacks.

---

## Table of Contents

<small>(Hand‑crafted; anchors match section numbers.)</small>

1. [Environment Setup](#1)
2. [Dash × Bootstrap Synergy](#2)
3. [Brand Palette & Theme](#3)
4. [Bootstrap Grid, Visually](#4)
5. [Row §1 — Header](#5)
6. [Row §2 — KPI Cards](#6)
7. [Row §3 — Data Tabs](#7)
8. [Row §4 — Dynamic Content Area](#8)
9. [Putting It All Together](#9)
10. [Responsiveness Lab](#10)
11. [Exercises & Further Reading](#11)

---

<a id="1"></a>

## 1 ▪︎ Environment Setup

*(code cell)*

```python
# OPTIONAL: auto‑reload helper modules during edits
# %load_ext autoreload
# %autoreload 2

from pathlib import Path

from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from jupyter_dash import JupyterDash  # Notebook‑friendly wrapper

APP_TITLE = "IMDB Data Analysis Dashboard"
BRAND_COLOR = "#deb522"  # 🟡 brand accent
THEME = dbc.themes.BOOTSTRAP  # can be swapped for CYBORG / DARKLY etc.

app = JupyterDash(__name__, external_stylesheets=[THEME],
                  title=APP_TITLE, suppress_callback_exceptions=True)
```

**Why `JupyterDash`?** Embeds the server in‑notebook, so each `run_server(mode="inline")` renders an iframe right below the cell.

---

<a id="2"></a>

## 2 ▪︎ Dash × Bootstrap Synergy

*(markdown + comparative table)*

| Concern             | Dash (React wrapper)                 | Bootstrap (CSS & JS)                           |
| ------------------- | ------------------------------------ | ---------------------------------------------- |
| Component hierarchy | Python objects → React DOM           | —                                              |
| Layout grid         | `html.Div`, `dcc.Tabs`, callbacks    | `dbc.Container / Row / Col` (12‑col flex grid) |
| Styling & theming   | Inline style dicts, CSS assets       | Pre‑styled components, dark theme variants     |
| Interactive state   | `@app.callback`, client‑side modules | —                                              |
| A11y / ARIA         | Provided by underlying React         | Provided by Bootstrap components               |

> **Mental model:** **Dash** = logic, state, reactivity. **Bootstrap** = pixel maths & design system.

### 2.1 Why not pure CSS grid?

Bootstrap’s grid *and* utility classes (`d‑flex`, `mt‑3`, etc.) give us **predictable breakpoints** without re‑inventing the wheel.

---

<a id="3"></a>

## 3 ▪︎ Brand Palette & Theme

*(markdown + code)*
We centralise colour constants to avoid magic strings and promote theming.

```python
COLORS = {
    "brand": BRAND_COLOR,
    "bg_dark": "#000000",
    "text_on_dark": "#f9f9f9",
    "danger": "#d9534f",   # Bootstrap red if we need alerts
}
```

Place your custom overrides in `./assets/theme.css` (loaded automatically by Dash).

Example snippet:

```css
body { background‑color: #000 !important; color: #f9f9f9; }
```

---

<a id="4"></a>

## 4 ▪︎ Bootstrap Grid, Visually

*(mermaid diagram)*

```mermaid
flowchart TB
  subgraph Container (max‑width varies by breakpoint)
    direction TB
    R1[Row §1 — Header]:::row
    R2[Row §2 — KPI Cards]:::row
    R3[Row §3 — Data Tabs]:::row
    R4[Row §4 — Dynamic Content]:::row
  end
  classDef row fill:#111,stroke:#555,color:#f9f9f9,stroke‑width:1px;
```

> The **12‑column philosophy**: every `dbc.Row` wraps one horizontal band; each `dbc.Col` claims 1–12 units, automatically wrapping on smaller screens.

---

<a id="5"></a>

## 5 ▪︎ Row §1 — Header

*(code + design notes)*

```python
header_row = dbc.Row([
    # Logo
    dbc.Col(html.Img(src="./assets/imdb.png", width=150), width=2,
            style={"paddingLeft": "1rem"}),

    # Primary nav tabs
    dbc.Col(
        dcc.Tabs(
            id="graph-tabs", value="overview",
            colors={
              "border": "#000000",
              "primary": COLORS["brand"],
              "background": "#000000",
            },
            children=[
                dcc.Tab(label="Overview",           value="overview"),
                dcc.Tab(label="Content creators",   value="content_creators"),
                dcc.Tab(label="Parental Guide",     value="parental"),
                dcc.Tab(label="Year",               value="year"),
            ],
            style={"marginTop": "15px", "width": "600px", "height": "50px"},
        ),
        width=6,
    ),
])
```

**Design rationale**

* **Whitespace**: 2‑column gutter left & right keeps logo from crowding on < 992 px.
* **Tab component**: `dcc.Tabs` + dark background + brand accent ensures clear affordance.

---

<a id="6"></a>

## 6 ▪︎ Row §2 — KPI Cards

*(helper function + code)*

```python
def stats_card(title: str, value, img: str):
    """Single KPI card, fully theme‑aware."""
    return dbc.Card([
        dbc.CardImg(src=img, top=True,
                     style={"width": "50px", "alignSelf": "center"}),
        dbc.CardBody([
            html.P(f"{value:,}", className="card‑value",
                   style={"margin": 0, "fontSize": "22px", "fontWeight": "bold"}),
            html.H4(title, className="card‑title",
                    style={"margin": 0, "fontSize": "18px", "fontWeight": "bold"}),
        ], style={"textAlign": "center"}),
    ], style={
        "paddingBlock": "10px",
        "backgroundColor": COLORS["brand"],
        "border": "none",
        "borderRadius": "10px",
    })
```

```python
kpi_row = dbc.Row([
    dbc.Col(stats_card("Work",          123_456, "./assets/movie-icon.png"),   width=3),
    dbc.Col(stats_card("Language",      48,      "./assets/language-icon.svg"), width=3),
    dbc.Col(stats_card("Country",       87,      "./assets/country-icon.png"),  width=3),
    dbc.Col(stats_card("Average Votes", 7.8,     "./assets/vote-icon.png"),     width=3),
], style={"marginBlock": "10px"})
```

**Responsive rule** — on `xs` screens (`<576 px`) Bootstrap auto‑stacks each `col` to full width.

---

<a id="7"></a>

## 7 ▪︎ Row §3 — Data Tabs

*(code)*

```python
data_tab_style = {
    "border": "1px solid white",
    "backgroundColor": "#000000",
    "color": COLORS["brand"],
    "fontWeight": "bold",
}

data_tabs = dbc.Row([
    dcc.Tabs(id="data-tabs", value="movie", style={"padding": 0}, children=[
        dcc.Tab(label="Movie",  value="movie",  style=data_tab_style,
                selected_style={**data_tab_style, "textDecoration": "underline"}),
        dcc.Tab(label="Series", value="series", style=data_tab_style,
                selected_style={**data_tab_style, "textDecoration": "underline"}),
    ])
])
```

> **Why a second tab bar?** Allows orthogonal switching: *what kind of content* vs *what analysis view*.

---

<a id="8"></a>

## 8 ▪︎ Row §4 — Dynamic Content Area

*(code)*

```python
dynamic_row = dbc.Row(
    dcc.Loading(
        html.Div(id="tabs-content"),
        type="default", color=COLORS["brand"],
    )
)
```

The loading spinner appears only while the chosen visualisation builder computes Plotly figures—crucial for good UX on slower notebooks or large data.

---

<a id="9"></a>

## 8 a ▪︎ Callback Workflow — How Visualisations Refresh

The **heart** of interactivity lives in a *single* Dash callback that reacts to both tab bars. Every time you change either tab, Dash:

1. Sends the current `value` of **`graph-tabs`** (analysis view) and **`data-tabs`** (Movie / Series) to Python.
2. Executes the callback function, which chooses the correct DataFrame(s) **and** the correct visualisation builder.
3. Returns freshly rendered Plotly figures that `dcc.Graph` then serialises to JSON for the browser.

### 8 a.1 The callback in `app.py`

```python
@app.callback(
    Output("tabs-content", "children"),
    Input("graph-tabs", "value"),
    Input("data-tabs", "value"),
)
def update_tab(graph_tab: str, data_tab: str):
    # 1 ▸ Pick dataset
    data, splits = DATA_BY_TAB[data_tab]

    # 2 ▸ Pick the correct generator and expected‑figure count
    builder, expected = VISUALIZATION_BUILDERS[graph_tab]

    # 3 ▸ Build figures
    figures = builder(data, splits)
    if len(figures) != expected:
        raise ValueError(
            f"{builder.__name__} returned {len(figures)} figs; expected {expected}")

    # 4 ▸ Wrap & return → Dash injects into <div id='tabs-content'>
    return wrap_figures(figures)
```

### 8 a.2 Why this pattern is **good practice**

| ✅ Benefit               | Explanation                                                                                                                      |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| **DRY**                 | One callback replaces four nearly identical `if/elif` blocks, reducing bugs & merge conflicts.                                   |
| **Declarative mapping** | `VISUALIZATION_BUILDERS` & `DATA_BY_TAB` act as look‑up tables—easier to read than nested conditionals.                          |
| **Early failure**       | The length check raises an exception if a visualisation returns the wrong # of figures, catching errors during dev.              |
| **Performance**         | Only the figures for the *currently* visible tab are computed—no wasted CPU/GPU cycles.                                          |
| **Extensibility**       | Adding a new analysis = write `generate_visualizations5`, register it, add a new tab label. *Zero* changes to the callback body. |
| **Unit‑testable**       | Because the builder functions are pure (`data_in → figures_out`), you can test them without Dash.                                |

> 🚀 **Take‑away:** A **single, declarative callback** scales better than many tab‑specific callbacks—fewer wires to tangle, easier mental model.

---

## 9 ▪︎ Putting It All Together

*(code cell)*

```python
app.layout = html.Div(
    dbc.Container([
        header_row,
        kpi_row,
        data_tabs,
        dynamic_row,
    ], style={"padding": 0}),
    style={"backgroundColor": COLORS["bg_dark"], "minHeight": "100vh"},
)
```

```python
# 🔄 Inline preview
app.run_server(mode="inline", debug=False, port=8050)
```

---

<a id="10"></a>

## 10 ▪︎ Responsiveness Lab

*(markdown)*

1. **Resize** the output pane or open the app in a new tab. Verify no horizontal scrollbars appear.
2. **iPhone SE simulation** in Chrome DevTools — KPI cards stack vertically, header logo shrinks gracefully.
3. **Landscape tablet** — cards show 2‑per‑row; nav tabs remain centred.

---

<a id="11"></a>

## 11 ▪︎ Exercises & Further Reading

*(markdown)*
\### Exercises

1. **Sticky footer**: Add a footer row with author credits that sticks to the bottom on tall screens.
2. **Sidebar variant**: Move both tab bars into a collapsible sidebar; test at ≥992 px breakpoints.
3. **ARIA audit**: Use Lighthouse A11y checks; ensure buttons & tabs have accessible names.

\### Reading list

* Dash docs → [https://dash.plotly.com](https://dash.plotly.com) (esp. Layout & Callback sections)
* Dash‑Bootstrap‑Components → [https://dash-bootstrap-components.opensource.faculty.ai](https://dash-bootstrap-components.opensource.faculty.ai)
* Bootstrap v5 Grid → [https://getbootstrap.com/docs/5.3/layout/grid/](https://getbootstrap.com/docs/5.3/layout/grid/)
* Plotly pits & tips → official blog articles on performance optimisation.

---

*© 2025 — IMDB Dashboard project*
'''

def parse_notebook_from_markdown(md_text):
    lines = md_text.splitlines(keepends=True)
    cells = []
    buffer = []
    in_code = False

    for line in lines:
        if line.strip().startswith("```"):
            if in_code:
                cells.append(nbf.v4.new_code_cell("".join(buffer)))
                buffer = []
                in_code = False
            else:
                if buffer:
                    cells.append(nbf.v4.new_markdown_cell("".join(buffer)))
                    buffer = []
                in_code = True
        else:
            buffer.append(line)

    if buffer:
        cell = nbf.v4.new_code_cell if in_code else nbf.v4.new_markdown_cell
        cells.append(cell("".join(buffer)))

    return nbf.v4.new_notebook(cells=cells)

notebook = parse_notebook_from_markdown(canvas_text)

# Save it
notebook_path = "01_layout_structure.ipynb"
with open(notebook_path, "w", encoding="utf-8") as f:
    nbf.write(notebook, f)

print(f"Notebook created: {notebook_path}")
