from dataclasses import dataclass
from datetime import date

import pandas as pd

# ----- Abstract -----
@dataclass
class AbstractData:
    contract_data: pd.DataFrame
    bid_data: pd.DataFrame
    bidder_data: pd.DataFrame


@dataclass
class TransformedContract:
    df: pd.DataFrame
    df_schema = {
        "letting_date": date,
        "job_description": str,
        "id": str,
        "sp_number": str,
        "distric": str,
        "county": str,
        "winning_bidder_id": str,
        "spec_year": str,
    }


@dataclass
class TransformedBid:
    df: pd.DataFrame
    df_schema = {
        "item_id": str,
        "long_description": str,
        "compound_item_id": str,
        "quanity": float,
        "bidder_id": str,
        "unit_price": int,
        "contract_id": str,
    }


@dataclass
class TransformedBidder:
    df: pd.DataFrame
    df_schema = {"id": str, "name": str}


# ----- Transport List -----
@dataclass
class ItemListData:
    df: pd.DataFrame


@dataclass
class TransformedItemList:
    df: pd.DataFrame
    df_schema = {
        "id": str,
        "compound_id": str,
        "short_description": str,
        "long_description": str,
        "short_unit": str,
        "long_unit": str,
        "spec_year": str,
    }


@dataclass
class SpecYearMatrix:
    df: pd.DataFrame
    df_schema = {
        "compound_item_id": str,
        "is_in_2016": bool,
        "is_in_2018": bool,
        "is_in_2020": bool,
    }
