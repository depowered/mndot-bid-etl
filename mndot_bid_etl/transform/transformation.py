from dataclasses import dataclass
from typing import Any, Callable, Protocol

import pandas as pd

TransformationFunction = Callable[[pd.DataFrame], pd.DataFrame]


class Transformation(Protocol):
    """Applies a pipeable, column-wise pandas.DataFrame method."""

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        """Returns a transformed dataframe."""


RenameFunction = Callable[[str], str]
RenameColumnsMapping = dict[str, str | RenameFunction]


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

    fuzzy_rename_map: RenameColumnsMapping

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        # Initialized an empty columns dict of structure {old_column_name: new_column_name}
        columns: dict[str, str] = {}

        # Iterate over each column of the input dataframe
        for column in df.columns.to_list():
            # Get the matching value from the fuzzy_rename_map
            for key, value in self.fuzzy_rename_map.items():
                if key in column:
                    # Append the columns dict with the {old_column_name: new_column_name} pair
                    if callable(value):
                        columns[column] = value(column)
                    else:
                        columns[column] = value

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


CastColumnsMapping = dict[str, str]


@dataclass
class CastColumns:
    """
    Provides a pipeable apply method that casts dataframe columns based on the provided list of dtype_map.

    Parameters
    ----------
    fuzzy_dtype_map : dict of search_string -> DType
        search_string : matches to column labels by the pattern `search_string in label == True`
        DType : Enum representing pandas compatible data types
    """

    fuzzy_dtype_map: CastColumnsMapping

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        # Intialize an empty dtype dict of structure {column_label: DType}
        dtype = {}

        # Iterate over each column of the input dataframe
        for column in df.columns.to_list():
            # Get the matching value from the fuzzy_dtype_map
            for search_string, destination_dtype in self.fuzzy_dtype_map.items():
                if search_string in column:
                    # Append the dtype dict with the {column_label: DType} pair
                    dtype[column] = destination_dtype

        # Execute the df.astype() method
        return df.astype(dtype=dtype)


ModifyValuesFunction = Callable[[Any], Any]
ModifyValuesMapping = dict[str, ModifyValuesFunction]


@dataclass
class ModifyValues:
    """
    Provides a pipeable apply method that transforms dataframe values based on
    column-to-function mappings provided in fuzzy_modify_map.

    Parameters
    ----------
    fuzzy_modify_map : dict of search_string -> modify_func
        search_string : matches to column labels by the pattern `search_string in label == True`
        modify_func : function to use for transforming the data
    """

    fuzzy_modify_map: ModifyValuesMapping

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        # Initialize an empty dataframe to store output columns
        out_df = pd.DataFrame()

        # Iterate over each column of the input dataframe
        for column in df.columns.to_list():
            # Get the matching function from the fuzzy_modify_map
            for search_string, modify_func in self.fuzzy_modify_map.items():
                # If there is a matching function, and append it to the output dataframe
                if search_string in column:
                    out_df[column] = df[column].apply(modify_func)
                    break
            # Else append the unmodified column to the output dataframe
            if column not in out_df.columns:
                out_df[column] = df[column]

        # Return the output dataframe
        return out_df


@dataclass
class Melt:
    id_vars: list[str]
    var_name: str
    value_name: str

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.melt(
            id_vars=self.id_vars, var_name=self.var_name, value_name=self.value_name
        )
