import pandas as pd
from mndot_bid_etl.dtype import DType


def transform_bidder(df: pd.DataFrame) -> pd.DataFrame:

    out_df = pd.DataFrame()

    out_df["id"] = df["Bidder Number"].astype(DType.INT64)
    out_df["name"] = df["Bidder Name"].str.strip()

    return out_df
