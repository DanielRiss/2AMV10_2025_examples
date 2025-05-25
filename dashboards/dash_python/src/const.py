import pandas as pd

def get_constants(movies, series, movies_splits, series_splits):
    """
    Return four key KPI values for the dashboard:
    1. Total number of works  (movies + series)
    2. Total unique countries represented
    3. Total unique languages represented
    4. Average votes (integer) across movies and series
    """

    # 1 ─ total works
    num_of_works = len(movies) + len(series)

    # 2 ─ unique countries (from both split files)
    countries = pd.concat(
        [movies_splits["country"]["country"], series_splits["country"]["country"]],
        ignore_index=True,
    )
    num_of_countries = countries.nunique()

    # 3 ─ unique languages
    languages = pd.concat(
        [movies_splits["language"]["language"], series_splits["language"]["language"]],
        ignore_index=True,
    )
    num_of_lang = languages.nunique()

    # 4 ─ average votes, rounded to int
    avg_votes = int((movies["votes"].mean() + series["votes"].mean()) / 2)

    return num_of_works, num_of_countries, num_of_lang, avg_votes
