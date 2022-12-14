from mndot_bid_etl.transform.transformation import (
    CastColumns,
    DType,
    FilterColumns,
    RenaneColumns,
)
from mndot_bid_etl.transform.transformer import Transformer

# ---------- Define Transformations ----------
filter_columns = FilterColumns(fuzzy_filter_list=["Bidder Number", "Bidder Name"])

rename_columns = RenaneColumns(
    fuzzy_rename_map={
        "Bidder Number": "id",
        "Bidder Name": "name",
    }
)

cast_columns = CastColumns(
    fuzzy_dtype_map={
        "id": DType.STRING,
        "name": DType.STRING,
    }
)


# ---------- Construct Transformer ----------
bidder_transformer = Transformer(
    transformation_functions=[
        filter_columns.apply,
        rename_columns.apply,
        cast_columns.apply,
    ]
)
