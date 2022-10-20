from functools import partial

import pandas as pd
from mndot_bid_etl.dtype import DType


def _format_price(price: str) -> int:
    cleaned_str = price.strip().replace("$", "").replace(",", "")
    return int(float(cleaned_str) * 100)


def _format_quantity(quantity: str) -> float:
    return float(quantity.strip())


def _assign_bid_type(bidder_id: int, winning_bidder_id: int) -> str:
    if bidder_id == 0:
        return "engineer"
    elif bidder_id == winning_bidder_id:
        return "winning"
    else:
        return "losing"


def _generate_unit_price_column_map(df: pd.DataFrame) -> dict[str, str]:
    # Create list of unit price source columns
    unit_price_columns = [
        column for column in df.columns.to_list() if "(Unit Price)" in column
    ]

    # Create map of {source_column: target_column}
    unit_price_column_map = {}
    for column in unit_price_columns:
        out_column_name = column.split(" ")[0].strip()

        if out_column_name == "Engineers":  # Engineer is bidder_id 0
            unit_price_column_map[column] = "0"
        else:
            unit_price_column_map[column] = str(int(out_column_name))

    return unit_price_column_map


def transform_bid(
    df: pd.DataFrame, spec_year: str, winning_bidder_id: int
) -> pd.DataFrame:

    out_df = pd.DataFrame()

    out_df["contract_id"] = df["ContractId"].astype(DType.INT64)
    out_df["spec_year"] = spec_year
    out_df["spec_year"] = out_df["spec_year"].astype(DType.STRING)
    out_df["spec_code"] = df["ItemNumber"].str.strip().str.slice(0, 4)
    out_df["unit_code"] = df["ItemNumber"].str.strip().str.slice(4, 7)
    out_df["item_code"] = df["ItemNumber"].str.strip().str.slice(8)
    out_df["quantity"] = df["Quantity"].apply(_format_quantity)

    unit_price_column_map = _generate_unit_price_column_map(df)

    # Create unit price columns in out_df
    for source_name, target_name in unit_price_column_map.items():
        out_df[target_name] = df[source_name]
        out_df[target_name] = out_df[target_name].apply(_format_price)

    melt_df = out_df.melt(
        id_vars=[
            "contract_id",
            "spec_year",
            "spec_code",
            "unit_code",
            "item_code",
            "quantity",
        ],
        var_name="bidder_id",
        value_name="unit_price",
    )
    melt_df["bidder_id"] = melt_df["bidder_id"].astype(DType.INT64)

    partial_assign_bid_type = partial(
        _assign_bid_type, winning_bidder_id=winning_bidder_id
    )

    melt_df["bid_type"] = (
        melt_df["bidder_id"].apply(partial_assign_bid_type).astype(DType.STRING)
    )

    return melt_df
