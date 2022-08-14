import pandas as pd
from mndot_bid_etl.transform.abstract import Abstract


def find_all_columns(df: pd.DataFrame, search_strings: list[str]) -> list[str]:
    matching_columns = []
    for column in df.columns.to_list():
        for substring in search_strings:
            if substring in column:
                matching_columns.append(column)
    return matching_columns


def get_transformed_bidder_df(abstract: Abstract) -> pd.DataFrame:
    bidder_df_raw = abstract.bidder_df.copy()

    # Drop unnecessary columns
    search_strings = ["Bidder Amount"]
    columns_to_drop = find_all_columns(bidder_df_raw, search_strings)
    bidder_df_dropped = bidder_df_raw.drop(columns=columns_to_drop)

    # Rename remaining columns
    rename_map = {"Bidder Number": "id", "Bidder Name": "name"}
    bidder_df_renamed = bidder_df_dropped.rename(columns=rename_map)

    return bidder_df_renamed
