import pandas as pd

def value_counts_df(series, top_n=10, col_name="value"):
    """
    Return a DataFrame with columns:
      <col_name>, count, percentage
    where <col_name> is the original category name.
    """
    counts = (
        series
        .value_counts()
        .head(top_n)
        .rename_axis(col_name)          # sets index name
        .reset_index(name="count")      # becomes a normal column
    )
    total = counts["count"].sum()
    counts["percentage"] = counts["count"] / total * 100
    return counts