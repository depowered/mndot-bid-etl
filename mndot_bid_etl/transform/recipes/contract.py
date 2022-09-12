from mndot_bid_etl.dtype import DType
from mndot_bid_etl.transform.schema import ColumnSchema, TransformationSchema
from mndot_bid_etl.transform.transformation import CastColumns, RenaneColumns
from mndot_bid_etl.transform.transformer import Transformer

# ---------- Define Transformation Schema ----------
contract_transformation_schema = TransformationSchema(
    [
        ColumnSchema(
            name="letting_date",
            dtype=DType.DATE,
            source_column_search_string="Letting Date",
        ),
        ColumnSchema(
            name="description",
            dtype=DType.STRING,
            source_column_search_string="Job Description",
        ),
        ColumnSchema(
            name="id", dtype=DType.STRING, source_column_search_string="Contract Id"
        ),
        ColumnSchema(
            name="sp_number",
            dtype=DType.STRING,
            source_column_search_string="SP Number",
        ),
        ColumnSchema(
            name="district", dtype=DType.STRING, source_column_search_string="District"
        ),
        ColumnSchema(
            name="county", dtype=DType.STRING, source_column_search_string="County"
        ),
    ]
)


# ---------- Create Transformations ----------
rename_columns = RenaneColumns(contract_transformation_schema.get_rename_columns_map())

cast_columns = CastColumns(contract_transformation_schema.get_cast_columns_map())


# ---------- Construct Transformer ----------
contract_transformer = Transformer(
    transformation_functions=[
        rename_columns.apply,
        cast_columns.apply,
    ]
)
