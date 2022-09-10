from mndot_bid_etl.transform.transformer import Transformer
from mndot_bid_etl.transform.transformation import (
    DType,
    RenaneColumns,
    CastColumns,
)


# ---------- Define Transformations ----------
rename_columns = RenaneColumns(
    fuzzy_rename_map={
        "Letting Date": lambda _: "letting_date",
        "Job Description": lambda _: "description",
        "Contract Id": lambda _: "id",
        "SP Number": lambda _: "sp_number",
        "District": lambda _: "district",
        "County": lambda _: "county",
    }
)

cast_columns = CastColumns(
    fuzzy_dtype_map={
        "letting_date": DType.DATE,
        "description": DType.STRING,
        "id": DType.STRING,
        "sp_number": DType.STRING,
        "district": DType.STRING,
        "county": DType.STRING,
    }
)


# ---------- Construct Transformer ----------
contract_transformer = Transformer(
    transformation_functions=[
        rename_columns.apply,
        cast_columns.apply,
    ]
)
