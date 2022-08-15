import pandas as pd


# ---------- Drop Functions ----------
def generate_drop_column_list(df: pd.DataFrame, search_strings: list[str]) -> list[str]:
    matching_columns = []
    for column in df.columns.to_list():
        for substring in search_strings:
            if substring in column:
                matching_columns.append(column)
    return matching_columns


def drop_bidder_columns(df: pd.DataFrame, search_strings: list[str]) -> pd.DataFrame:
    drop_columns = generate_drop_column_list(df, search_strings)
    return df.drop(columns=drop_columns)


# ---------- Rename Functions ----------
def rename_bidder_columns(df: pd.DataFrame) -> pd.DataFrame:
    mapper = {"Bidder Number": "id", "Bidder Name": "name"}
    return df.rename(columns=mapper)


# ---------- Transform Pipeline ----------
def transform_bidder_df(df: pd.DataFrame) -> pd.DataFrame:
    # Drop unnecessary columns
    search_strings = ["Bidder Amount"]

    return df.pipe(drop_bidder_columns, search_strings).pipe(rename_bidder_columns)
