from mndot_bid_etl.transform.transformer import Transformer
from mndot_bid_etl.transform.transformation import (
    DType,
    FilterColumns,
    RenaneColumns,
    CastColumns,
)


# ---------- Define Transformations ----------
filter_columns = FilterColumns(fuzzy_filter_list=["Bidder Number", "Bidder Name"])

rename_columns = RenaneColumns(
    fuzzy_rename_map={
        "Bidder Number": lambda _: "id",
        "Bidder Name": lambda _: "name",
    }
)

cast_columns = CastColumns(
    fuzzy_dtype_map={
        "id": DType.STRING,
        "name": DType.STRING,
    }
)


# ---------- Construct Bid Transformer ----------
bidder_transformer = Transformer(
    transformation_functions=[
        filter_columns.apply,
        rename_columns.apply,
        cast_columns.apply,
    ]
)
