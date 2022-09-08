from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Protocol
import pandas as pd


class Transformation(Protocol):
    """Applies a pipeable, column-wise pandas.DataFrame method."""

    def apply(df: pd.DataFrame) -> pd.DataFrame:
        """Returns a transformed dataframe."""


@dataclass
class RenaneColumns:
    rename_map: dict[str, Callable[[str], str]]

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        # Initialized an empty columns dict of structure {old_column_name: new_column_name}
        columns: dict[str, str] = {}

        # Iterate over each column of the input dataframe
        for column in df.columns.to_list():
            # Get the matching value from the rename_map
            for search_string, func in self.rename_map.items():
                if search_string in column:
                    # Append the columns dict with the {old_column_name: new_column_name} pair
                    columns[column] = func(column)

        # Execture the df.rename() method
        return df.rename(columns=columns)


@dataclass
class FilterColumns:
    filter_list: list[str]

    def apply(df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError()


class DType(Enum):
    DTYPE = "dtype"


@dataclass
class CastColumns:
    dtype_map: dict[str, DType]

    def apply(df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError()


@dataclass
class ModifyValues:
    format_map: dict[str, Callable[[Any], Any]]

    def apply(df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError()


@dataclass
class Melt:
    id_vars: list[str]
    var_name: str
    value_name: str

    def apply(df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError()
