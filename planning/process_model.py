from typing import Any
from pathlib import Path
import pandas as pd

from .data_model import AbstractData, ItemListData, SpecYearMatrix, TransformedItemList


# ----- Readers -----
def read_abstract_data_from_csv(file_path: Path) -> AbstractData:
    """Reads an abstract CSV file to an AbstractData container."""
    raise NotImplementedError()


def read_item_list_data_from_csv(file_path: Path) -> ItemListData:
    """Reads an item list CSV file to an ItemListData container."""
    raise NotImplementedError()


def read_spec_year_matrix_from_csv(file_path: Path) -> SpecYearMatrix:
    """Reads a spec year matrix CSV file to a SpecYearMatrix container."""
    raise NotImplementedError()


# ----- Transformers -----
def transform_contract_data(
    contract_data: pd.DataFrame, winning_bidder_id: str, spec_year: str
) -> pd.DataFrame:
    raise NotImplementedError()


def transform_bid_data(bid_data: pd.DataFrame) -> pd.DataFrame:
    raise NotImplementedError()


def transorm_bidder_data(bidder_data: pd.DataFrame) -> pd.DataFrame:
    raise NotImplementedError()


def tranform_item_list(item_list: pd.DataFrame) -> pd.DataFrame:
    raise NotImplementedError()


def generate_spec_year_matrix(
    transformed_item_lists: list[pd.DataFrame],
) -> pd.DataFrame:
    raise NotImplementedError()


# ----- Writers -----
def write_dataframe_to_csv(data: pd.DataFrame, file_path: Path, **kwargs: Any) -> None:
    with open(file_path, "w") as f:
        data.to_csv(f, **kwargs)
