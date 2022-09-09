from mndot_bid_etl.transform.transformer import Transformer
from mndot_bid_etl.transform.transformation import (
    DType,
    FilterColumns,
    RenaneColumns,
    ModifyValues,
    Melt,
    CastColumns,
)


# ---------- Format Functions ----------
def format_item_id(id: str) -> str:
    return id[:4] + "." + id[4:]


def format_long_description(long_description: str) -> str:
    return long_description.strip().replace("''", '"')


def format_quantity(quantity: str) -> float:
    return float(quantity.strip())


def format_price(price: str) -> int:
    cleaned_str = price.strip().replace("$", "").replace(",", "")
    return int(float(cleaned_str) * 100)


# ---------- Define Transformations ----------
filter_columns = FilterColumns(
    fuzzy_filter_list=[
        "ContractId",
        "ItemNumber",
        "ItemDescription",
        "Quantity",
        "(Unit Price)",
    ]
)

modify_values = ModifyValues(
    fuzzy_modify_map={
        "ItemNumber": format_item_id,
        "ItemDescription": format_long_description,
        "Quantity": format_quantity,
        "(Unit Price)": format_price,
    }
)

rename_columns = RenaneColumns(
    fuzzy_rename_map={
        "ContractId": lambda _: "contract_id",
        "ItemNumber": lambda _: "item_id",
        "ItemDescription": lambda _: "long_description",
        "Quantity": lambda _: "quantity",
        "(Unit Price)": lambda x: x.strip().split(" ")[0].lower(),
    }
)


melt = Melt(
    id_vars=["contract_id", "item_id", "long_description", "quantity"],
    var_name="bidder_id",
    value_name="unit_price",
)


cast_columns = CastColumns(
    fuzzy_dtype_map={
        "contract_id": DType.STRING,
        "item_id": DType.STRING,
        "long_description": DType.STRING,
        "quantity": DType.FLOAT64,
        "bidder_id": DType.STRING,
        "unit_price": DType.INT64,
    }
)


# ---------- Construct Bid Transformer ----------
bid_transformer = Transformer(
    transformation_functions=[
        filter_columns.apply,
        modify_values.apply,
        rename_columns.apply,
        melt.apply,
        cast_columns.apply,
    ]
)
