from mndot_bid_etl.transform.schema import ColumnSchema, TransformationSchema
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


# ---------- Define Transformation Schema ----------
item_transformation_schema = TransformationSchema(
    [
        ColumnSchema(
            name="id", dtype=DType.STRING, source_column_search_string="Item Number"
        ),
        ColumnSchema(
            name="description",
            dtype=DType.STRING,
            source_column_search_string="Short Description",
            modify_value_func=format_description,
        ),
        ColumnSchema(
            name="long_description",
            dtype=DType.STRING,
            source_column_search_string="Long Description",
            modify_value_func=format_description,
        ),
        ColumnSchema(
            name="unit", dtype=DType.STRING, source_column_search_string="Unit Name"
        ),
        ColumnSchema(
            name="unit_description",
            dtype=DType.STRING,
            source_column_search_string="Plan Unit Description",
        ),
        ColumnSchema(
            name="spec_year",
            dtype=DType.STRING,
            source_column_search_string="Spec Year",
            modify_value_func=format_spec_year,
        ),
    ]
)


# ---------- Create Transformations ----------
filter_columns = FilterColumns(
    item_transformation_schema.get_filter_columns_list(
        use_source_column_search_string=True
    )
    # fuzzy_filter_list=[
    #     "Item Number",
    #     "Short Description",
    #     "Long Description",
    #     "Unit Name",
    #     "Plan Unit Description",
    #     "Spec Year",
    # ]
)

rename_columns = RenaneColumns(
    item_transformation_schema.get_rename_columns_map()
    # fuzzy_rename_map={
    #     "Item Number": "id",
    #     "Short Description": "description",
    #     "Long Description": "long_description",
    #     "Unit Name": "unit",
    #     "Plan Unit Description": "unit_description",
    #     "Spec Year": "spec_year",
    # }
)

modify_values = ModifyValues(
    item_transformation_schema.get_modify_values_map()
    # fuzzy_modify_map={
    #     "description": format_description,
    #     "long_description": format_description,
    #     "spec_year": format_spec_year,
    # }
)

cast_columns = CastColumns(
    item_transformation_schema.get_cast_columns_map()
    # fuzzy_dtype_map={
    #     "id": DType.STRING,
    #     "description": DType.STRING,
    #     "long_description": DType.STRING,
    #     "unit": DType.STRING,
    #     "unit_description": DType.STRING,
    #     "spec_year": DType.STRING,
    # }
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
