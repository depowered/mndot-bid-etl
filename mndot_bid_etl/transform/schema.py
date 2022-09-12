from dataclasses import dataclass
from typing import Any, Callable, Optional

from mndot_bid_etl.transform.transformation import (
    CastColumnsMapping,
    ModifyValuesMapping,
    RenameColumnsMapping,
)


@dataclass
class ColumnSchema:
    name: str
    dtype: str
    source_column_search_string: str
    rename_func: Optional[Callable[[str], str]] = None
    modify_value_func: Optional[Callable[[Any], Any]] = None


@dataclass
class TransformationSchema:
    column_schemas: list[ColumnSchema]

    def get_filter_columns_list(
        self, use_source_column_search_string: bool = False
    ) -> list[str]:
        """
        Returns a list of columns to filter.

        Parameters
        ----------
        use_source_column_search_string : bool, default False
            Use the source_column_search_string to identify the columns to be filtered.
        """

        if use_source_column_search_string:
            return [
                column.source_column_search_string for column in self.column_schemas
            ]
        return [column.name for column in self.column_schemas]

    def get_modify_values_map(
        self, use_source_column_search_string: bool = False
    ) -> ModifyValuesMapping:
        """
        Returns a dict of { column_name : ModifyValuesFunction }

        Parameters
        ----------
        use_source_column_search_string : bool, default False
            Use the source_column_search_string for the dict keys.
        """

        if use_source_column_search_string:
            return {
                schema.source_column_search_string: schema.modify_value_func
                for schema in self.column_schemas
                if schema.modify_value_func
            }
        return {
            schema.name: schema.modify_value_func
            for schema in self.column_schemas
            if schema.modify_value_func
        }

    def get_rename_columns_map(self) -> RenameColumnsMapping:
        """
        Returns a dict of { source_column_search_string : column_name | rename_func }
        """

        mapping: RenameColumnsMapping = {}
        for schema in self.column_schemas:
            if schema.rename_func:
                mapping[schema.source_column_search_string] = schema.rename_func
            else:
                mapping[schema.source_column_search_string] = schema.name

        return mapping

    def get_cast_columns_map(
        self, use_source_column_search_string: bool = False
    ) -> CastColumnsMapping:
        """
        Returns a dict of { column_name : DType.value }

        Parameters
        ----------
        use_source_column_search_string : bool, default False
            Use the source_column_search_string for the dict keys.
        """

        if use_source_column_search_string:
            return {
                schema.source_column_search_string: schema.dtype
                for schema in self.column_schemas
            }

        return {schema.name: schema.dtype for schema in self.column_schemas}
