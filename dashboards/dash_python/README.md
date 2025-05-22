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

## 🧠 Learning Through Notebooks

Instead of reading through long scripts, you’ll learn by stepping through structured Jupyter notebooks in the `notebooks/` folder:

| Notebook                              | Description                                                 |
| ------------------------------------- | ----------------------------------------------------------- |
| `00_dashboard_intro.ipynb`            | What this dashboard does, and how the components connect    |
| `01_layout_structure.ipynb`           | How the layout is built with Dash + Bootstrap               |
| `02_helper_functions.ipynb`           | Why and how we use helpers (e.g. KPI cards)                 |
| `03_tabs_and_callbacks.ipynb`         | How to switch between tabs and load dynamic content         |
| `04_visualization_helpers.ipynb`      | How each tab generates its graphs from data                 |
| `05_constants_and_data_loading.ipynb` | How the KPI values are calculated from data                 |
| `06_customization_tips.ipynb`         | How to tweak icons, styles, and layout for your own project |
| `07_deploying_and_adapting.ipynb`     | How to run the dashboard and adapt it to a new dataset      |

Each notebook includes:

* Real code snippets from the IMDb example
* Explanations of how/why it works
* Editable code cells for experimentation

---

## 🚀 Running the Dashboard

After exploring the notebooks, you can launch the working dashboard like this:

```bash
cd dashboards/dash_python
python app.py
```

Then open [http://127.0.0.1:8050](http://127.0.0.1:8050) in your browser.

---

## 🛠 Adapting the Template to Your Own Project

1. **Replace the dataset**
   Drop your own `.csv` or `.xlsx` files in the `data/` folder and update the file paths in `app.py`.

2. **Adjust KPI logic**
   Edit `src/const.py` to reflect the key metrics from your new data.

3. **Update visuals per tab**
   Modify `src/dash1.py` to `src/dash4.py` to generate charts using your new columns.
   If needed, add new tab modules and link them in `app.py`.

4. **Keep or remove recommendation**
   If you don’t need it, delete the related callbacks and dropdowns. Otherwise, update the similarity logic in the `movie-dropdown` and `series-dropdown` callbacks.

5. **Customize the design**
   Swap out the icons in `assets/`, or optionally add a `style.css` to the same folder for custom fonts/colors.

---

## ✅ Credits & Attribution

This template is based on [Mahmoud2227/IMDB-Dashboard](https://github.com/Mahmoud2227/IMDB-Dashboard), simplified and expanded with educational material.

Licensed for educational use in 2AMV10 – Visual Analytics.

---

## 👩‍💻 Contribute or Ask Questions

If something is unclear or you want extra examples, contact the student assistants: **Daniël Ris** or **Nora Bouwman**. You can also fork the repo and send improvement suggestions.