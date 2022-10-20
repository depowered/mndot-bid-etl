import re
from dataclasses import dataclass
from datetime import date
from io import StringIO
from pathlib import Path

import pandas as pd
from mndot_bid_etl.dtype import DType


@dataclass
class AbstractData:
    contract_df: pd.DataFrame
    bid_df: pd.DataFrame
    bidder_df: pd.DataFrame

    @property
    def contract_id(self) -> str:
        return self.contract_df.at[0, "Contract Id"]

    @property
    def winning_bidder_id(self) -> str:
        return self.bidder_df.at[0, "Bidder Number"]

    @property
    def letting_date(self) -> date:
        return (
            self.contract_df.astype({"Letting Date": "datetime64[ns]"})
            .at[0, "Letting Date"]
            .date()
        )


def create_abstract_data_from_csv(file: Path) -> AbstractData:
    """Creates an AbstractData object from csv."""

    def split_csv(file: Path) -> list[str]:
        """Splits the csv data by blank lines to divide into its three subtables."""
        blank_line_regex = r"(?:\r?\n){2,}"
        with open(file, "r") as f:
            return re.split(blank_line_regex, f.read())

    contract_data, bid_data, bidder_data = split_csv(file)

    contract_df = pd.read_csv(
        StringIO(contract_data), dtype=DType.STRING, escapechar="\\"
    )

    bid_df = pd.read_csv(StringIO(bid_data), dtype=DType.STRING, escapechar="\\")

    bidder_df = pd.read_csv(StringIO(bidder_data), dtype=DType.STRING, escapechar="\\")

    return AbstractData(contract_df, bid_df, bidder_df)
