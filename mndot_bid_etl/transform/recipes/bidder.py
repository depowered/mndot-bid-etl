from mndot_bid_etl.transform.schema import ColumnSchema, TransformationSchema
from mndot_bid_etl.transform.transformation import (
    CastColumns,
    DType,
    FilterColumns,
    RenaneColumns,
)
from mndot_bid_etl.transform.transformer import Transformer

# ---------- Define Transformation Schema ----------
bidder_transformation_schema = TransformationSchema(
    [
        ColumnSchema(
            name="id",
            dtype=DType.STRING,
            source_column_search_string="Bidder Number",
        ),
        ColumnSchema(
            name="name", dtype=DType.STRING, source_column_search_string="Bidder Name"
        ),
    ]
)

# ---------- Create Transformations ----------
filter_columns = FilterColumns(
    bidder_transformation_schema.get_filter_columns_list(
        use_source_column_search_string=True
    )
)

rename_columns = RenaneColumns(bidder_transformation_schema.get_rename_columns_map())

cast_columns = CastColumns(bidder_transformation_schema.get_cast_columns_map())


# ---------- Construct Transformer ----------
bidder_transformer = Transformer(
    transformation_functions=[
        filter_columns.apply,
        rename_columns.apply,
        cast_columns.apply,
    ]
)
