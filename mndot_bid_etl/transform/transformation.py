from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Protocol
import pandas as pd


class Transformation(Protocol):
    """Applies a pipeable, column-wise pandas.DataFrame method."""

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        """Returns a transformed dataframe."""


@dataclass
class RenaneColumns:
    """
    Provides a pipeable apply method that alters column labels based on the provided rename_map.

    Parameters
    ----------
    rename_map : dict of search_string -> nename_func
        search_string : matches to column labels by the pattern `search_string in label == True`
        rename_func : function that receives the existing column label and returns the renamed column label
    """

    fuzzy_rename_map: dict[str, Callable[[str], str]]

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        # Initialized an empty columns dict of structure {old_column_name: new_column_name}
        columns: dict[str, str] = {}

        # Iterate over each column of the input dataframe
        for column in df.columns.to_list():
            # Get the matching value from the fuzzy_rename_map
            for search_string, func in self.fuzzy_rename_map.items():
                if search_string in column:
                    # Append the columns dict with the {old_column_name: new_column_name} pair
                    columns[column] = func(column)

        # Execture the df.rename() method
        return df.rename(columns=columns)


@dataclass
class FilterColumns:
    """
    Provides a pipeable apply method that filters dataframe columns based on the provided list of search strings.

    Parameters
    ----------
    filter_list : list of search_string
        search_string : matches to column labels by the pattern `search_string in label == True`
    """

    fuzzy_filter_list: list[str]

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        # Intialize an empty items list
        items: list[str] = []

        # Iterate over each column of the input dataframe
        for column in df.columns.to_list():
            for search_string in self.fuzzy_filter_list:
                # Determine if the column label matches a string in fuzzy_filter_list
                if search_string in column:
                    # Append matching column labels to items list
                    items.append(column)

        # Execute the df.filter() method
        return df.filter(items=items)


class DType(Enum):
    STRING = "string"
    INT64 = "int64"
    FLOAT64 = "float64"
    BOOL = "boolean"
    DATE = "datetime64[ns]"


@dataclass
class CastColumns:
    """
    Provides a pipeable apply method that casts dataframe columns based on the provided list of dtype_map.

    Parameters
    ----------
    fuzzy_dtype_map : dict of search_string -> DType
        search_string : matches to column labels by the pattern `search_string in label == True`
    """

    fuzzy_dtype_map: dict[str, DType]

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        # Intialize an empty dtype dict of structure {column_label: DType.value}
        dtype = {}

        # Iterate over each column of the input dataframe
        for column in df.columns.to_list():
            # Get the matching value from the fuzzy_dtype_map
            for search_string, destination_dtype in self.fuzzy_dtype_map.items():
                if search_string in column:
                    # Append the dtype dict with the {column_label: DType.value} pair
                    dtype[column] = destination_dtype.value

        # Execute the df.astype() method
        return df.astype(dtype=dtype)


@dataclass
class ModifyValues:
    format_map: dict[str, Callable[[Any], Any]]

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError()


@dataclass
class Melt:
    id_vars: list[str]
    var_name: str
    value_name: str

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError()
