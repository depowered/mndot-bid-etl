import re
from dataclasses import dataclass
from datetime import date
from io import StringIO
from pathlib import Path

import pandas as pd


@dataclass
class Abstract:
    contract_df: pd.DataFrame
    bid_df: pd.DataFrame
    bidder_df: pd.DataFrame

    def __post_init__(self) -> None:
        # TODO: Write an actual method for determining spec year
        self.spec_year = "2001"

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


def split_csv(csv_file: Path) -> list[str]:
    """Splits the csv data by blank lines to divide into its three subtables"""
    blank_line_regex = r"(?:\r?\n){2,}"
    with open(csv_file, "r") as f:
        return re.split(blank_line_regex, f.read())


def read_abstract_csv(csv_file: Path) -> Abstract:
    contract_data, bid_data, bidder_data = split_csv(csv_file)

    return Abstract(
        contract_df=pd.read_csv(
            StringIO(contract_data), dtype="object", escapechar="\\"
        ),
        bid_df=pd.read_csv(StringIO(bid_data), dtype="object", escapechar="\\"),
        bidder_df=pd.read_csv(StringIO(bidder_data), dtype="object", escapechar="\\"),
    )
