from mndot_bid_etl.transform.transformation import CastColumns, DType, RenaneColumns
from mndot_bid_etl.transform.transformer import Transformer

# ---------- Define Transformations ----------
rename_columns = RenaneColumns(
    fuzzy_rename_map={
        "Letting Date": "letting_date",
        "Job Description": "description",
        "Contract Id": "id",
        "SP Number": "sp_number",
        "District": "district",
        "County": "county",
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
