# Dash Python – IMDb Dashboard (Template & Tutorial)

This folder contains a **structured Dash application** inspired by the [IMDb Dashboard](https://github.com/Mahmoud2227/IMDB-Dashboard), reworked to serve as a **teaching template** for the 2AMV10 Visual Analytics course.

Instead of dumping all code in one place, this repository walks you through each step of the dashboard using **interactive notebooks**, **clear modular code**, and **real working examples**. The goal is not just to *run* the dashboard but to help you learn to *build your own*.

---

## Folder Structure

```text
dash_python/
├── app.py                     # Main Dash app (minimal logic, loads layout + callbacks)
├── src/                       # Visual modules (imported in app.py)
│   ├── const.py               # KPI constants
│   ├── dash1.py → dash4.py    # Charts for each tab
├── data/                      # Sample IMDb data (movies + series)
│   ├── movie_after_cleaning.csv
│   ├── series_after_cleaning.csv
│   ├── splits_movie.xlsx
│   └── splits_series.xlsx
├── assets/                    # Dashboard images/icons
│   ├── movie-icon.png
│   ├── vote-icon.png
│   ├── country-icon.png
│   ├── language-icon.svg
│   └── imdb.png
└── notebooks/                 # Explanatory notebooks (see below)
```

---

## Learning Through Notebooks

Instead of reading through long scripts, you’ll learn by stepping through structured Jupyter notebooks in the `notebooks/` folder:

| Notebook                      | Description                                                                                   |
| ----------------------------- | --------------------------------------------------------------------------------------------- |
| `00_project_startup.ipynb`    | How we load the data, compute KPIs, use helper functions, and define shared styles            |
| `01_layout_structure.ipynb`   | How we structure the layout using Dash & Bootstrap, and connect it to tab-based callback logic |
| `02_building_viz_functinos.ipynb` | How each tab’s graphs are generated using Plotly in `dash1.py`–`dash4.py` modules             |


Each notebook includes:

* Real code snippets from the IMDb example
* Explanations of how/why it works
* Editable code cells for experimentation

---

## Running the Dashboard

After exploring the notebooks, you can launch the working dashboard like this:

```bash
cd dashboards/dash_python
python app.py
```

Then open [http://127.0.0.1:8050](http://127.0.0.1:8050) in your browser.

---

## Credits & Attribution

This template is based on [Mahmoud2227/IMDB-Dashboard](https://github.com/Mahmoud2227/IMDB-Dashboard), simplified and expanded with educational material.

---

##  Contribute or Ask Questions

If something is unclear or you want extra examples, contact the student assistants: **Daniël Ris** or **Nora Bouwman**. You can also fork the repo and send improvement suggestions.
