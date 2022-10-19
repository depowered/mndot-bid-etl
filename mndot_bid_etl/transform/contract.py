import pandas as pd
from mndot_bid_etl.dtype import DType


def transform_contract(
    df: pd.DataFrame, winning_bidder_id: int, spec_year: str
) -> pd.DataFrame:

    out_df = pd.DataFrame()

    out_df["id"] = df["Contract Id"].astype(DType.INT64)
    out_df["letting_date"] = pd.to_datetime(df["Letting Date"])
    out_df["sp_number"] = df["SP Number"].str.strip()
    out_df["district"] = df["District"].str.strip().str.title()
    out_df["county"] = df["County"].str.strip().str.title()
    out_df["description"] = df["Job Description"].str.strip()
    out_df["winning_bidder_id"] = winning_bidder_id
    out_df["spec_year"] = spec_year
    out_df["spec_year"] = out_df["spec_year"].astype(DType.STRING)

    return out_df
