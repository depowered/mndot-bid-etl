import re
import pandas as pd
from dataclasses import dataclass
from pathlib import Path
from io import StringIO


@dataclass
class Abstract:
    contract_df: pd.DataFrame
    bid_df: pd.DataFrame
    bidder_df: pd.DataFrame

    @property
    def contract_id(self) -> str:
        return self.contract_df.at[0, "Contract Id"]

    @property
    def winning_bidder_id(self) -> str:
        return self.bidder_df.at[0, "Bidder Number"]


def split_csv(csv_file) -> list[str]:
    """Splits the csv data by blank lines to divide into its three subtables"""
    blank_line_regex = r"(?:\r?\n){2,}"
    with open(csv_file, "r") as f:
        return re.split(blank_line_regex, f.read())


def read_csv(csv_file: Path) -> Abstract:
    contract_data, bid_data, bidder_data = split_csv(csv_file)

    return Abstract(
        contract_df=pd.read_csv(StringIO(contract_data), dtype="object"),
        bid_df=pd.read_csv(StringIO(bid_data), dtype="object"),
        bidder_df=pd.read_csv(StringIO(bidder_data), dtype="object"),
    )
