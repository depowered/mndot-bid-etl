from mndot_bid_etl.transform.transformation import (
    CastColumns,
    DType,
    FilterColumns,
    ModifyValues,
    RenaneColumns,
)
from mndot_bid_etl.transform.transformer import Transformer


# ---------- Format Functions ----------
def format_spec_year(two_digit_year: str) -> str:
    return "20" + two_digit_year


def format_description(desc: str) -> str:
    return desc.strip().replace(";", ",")


# ---------- Define Transformations ----------
filter_columns = FilterColumns(
    fuzzy_filter_list=[
        "Item Number",
        "Short Description",
        "Long Description",
        "Unit Name",
        "Plan Unit Description",
        "Spec Year",
    ]
)

rename_columns = RenaneColumns(
    fuzzy_rename_map={
        "Item Number": "id",
        "Short Description": "description",
        "Long Description": "long_description",
        "Unit Name": "unit",
        "Plan Unit Description": "unit_description",
        "Spec Year": "spec_year",
    }
)

modify_values = ModifyValues(
    fuzzy_modify_map={
        "description": format_description,
        "long_description": format_description,
        "spec_year": format_spec_year,
    }
)

cast_columns = CastColumns(
    fuzzy_dtype_map={
        "id": DType.STRING,
        "description": DType.STRING,
        "long_description": DType.STRING,
        "unit": DType.STRING,
        "unit_description": DType.STRING,
        "spec_year": DType.STRING,
    }
)


# ---------- Construct Transformer ----------
item_transformer = Transformer(
    transformation_functions=[
        filter_columns.apply,
        rename_columns.apply,
        modify_values.apply,
        cast_columns.apply,
    ]
)
