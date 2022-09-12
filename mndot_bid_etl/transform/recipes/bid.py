from mndot_bid_etl.transform.schema import ColumnSchema, TransformationSchema
from mndot_bid_etl.transform.transformation import (
    CastColumns,
    DType,
    FilterColumns,
    Melt,
    ModifyValues,
    RenaneColumns,
)
from mndot_bid_etl.transform.transformer import Transformer


# ---------- Helper Functions ----------
def format_item_id(id: str) -> str:
    return id[:4] + "." + id[4:]


def format_long_description(long_description: str) -> str:
    return long_description.strip().replace("''", '"')


def format_quantity(quantity: str) -> float:
    return float(quantity.strip())


def format_price(price: str) -> int:
    cleaned_str = price.strip().replace("$", "").replace(",", "")
    return int(float(cleaned_str) * 100)


def rename_bidder_ids(name: str) -> str:
    return name.strip().split(" ")[0].lower()


bid_transformation_schema = TransformationSchema(
    column_schemas=[
        ColumnSchema(
            name="contract_id",
            dtype=DType.STRING,
            source_column_search_string="ContractId",
        ),
        ColumnSchema(
            name="item_id",
            dtype=DType.STRING,
            source_column_search_string="ItemNumber",
            modify_value_func=format_item_id,
        ),
        ColumnSchema(
            name="long_description",
            dtype=DType.STRING,
            source_column_search_string="ItemDescription",
            modify_value_func=format_long_description,
        ),
        ColumnSchema(
            name="quantity",
            dtype=DType.FLOAT64,
            source_column_search_string="Quantity",
            modify_value_func=format_quantity,
        ),
        ColumnSchema(
            name="bidder_id",
            dtype=DType.STRING,
            source_column_search_string="(Unit Price)",
            modify_value_func=format_price,
            rename_func=rename_bidder_ids,
        ),
    ]
)


# ---------- Define Transformations ----------
filter_columns = FilterColumns(
    fuzzy_filter_list=bid_transformation_schema.get_filter_columns_list(
        use_source_column_search_string=True
    )
    # fuzzy_filter_list=[
    #     "ContractId",
    #     "ItemNumber",
    #     "ItemDescription",
    #     "Quantity",
    #     "(Unit Price)",
    # ]
)

modify_values = ModifyValues(
    fuzzy_modify_map=bid_transformation_schema.get_modify_values_map(
        use_source_column_search_string=True
    )
    # fuzzy_modify_map={
    #     "ItemNumber": format_item_id,
    #     "ItemDescription": format_long_description,
    #     "Quantity": format_quantity,
    #     "(Unit Price)": format_price,
    # }
)

rename_columns = RenaneColumns(
    fuzzy_rename_map=bid_transformation_schema.get_rename_columns_map()
    # fuzzy_rename_map={
    #     "ContractId": "contract_id",
    #     "ItemNumber": "item_id",
    #     "ItemDescription": "long_description",
    #     "Quantity": "quantity",
    #     "(Unit Price)": lambda x: x.strip().split(" ")[0].lower(),
    # }
)


melt = Melt(
    id_vars=["contract_id", "item_id", "long_description", "quantity"],
    var_name="bidder_id",
    value_name="unit_price",
)


cast_columns = CastColumns(
    fuzzy_dtype_map=bid_transformation_schema.get_cast_columns_map()
    # fuzzy_dtype_map={
    #     "contract_id": DType.STRING,
    #     "item_id": DType.STRING,
    #     "long_description": DType.STRING,
    #     "quantity": DType.FLOAT64,
    #     "bidder_id": DType.STRING,
    #     "unit_price": DType.INT64,
    # }
)


# ---------- Construct Transformer ----------
bid_transformer = Transformer(
    transformation_functions=[
        filter_columns.apply,
        modify_values.apply,
        rename_columns.apply,
        melt.apply,
        cast_columns.apply,
    ]
)
