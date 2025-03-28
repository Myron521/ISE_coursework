import pandas as pd

def merge_title_body(data):
    """
    Merge Title and Body into a single column; if Body is NaN, use Title only.
    """
    data['Title+Body'] = data.apply(
        lambda row: row['Title'] + '. ' + row['Body'] if pd.notna(row['Body']) else row['Title'],
        axis=1
    )
    return data

def select_columns(data):
    """
    Keep only necessary columns: id, Number, sentiment, text (merged Title+Body).
    """
    data = data.rename(columns={
        "Unnamed: 0": "id",
        "class": "sentiment",
        "Title+Body": "text"
    })
    return data[["id", "Number", "sentiment", "text"]]