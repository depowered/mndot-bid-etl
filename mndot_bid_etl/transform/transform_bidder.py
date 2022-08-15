import pandas as pd


# ---------- Filter Column Functions ----------
def filter_bidder_columns(df: pd.DataFrame) -> pd.DataFrame:
    filter_columns = ["Bidder Number", "Bidder Name"]
    return df.filter(items=filter_columns, axis="columns")


# ---------- Rename Functions ----------
def rename_bidder_columns(df: pd.DataFrame) -> pd.DataFrame:
    mapper = {"Bidder Number": "id", "Bidder Name": "name"}
    return df.rename(columns=mapper)


# ---------- Transform Pipeline ----------
def transform_bidder_df(df: pd.DataFrame) -> pd.DataFrame:
    return df.pipe(filter_bidder_columns).pipe(rename_bidder_columns)
