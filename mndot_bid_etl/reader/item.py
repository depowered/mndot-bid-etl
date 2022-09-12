from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from mndot_bid_etl.dtype import DType


@dataclass
class ItemData:
    df: pd.DataFrame


def create_item_data_from_csv(file: Path) -> ItemData:
    with open(file, "r") as f:
        df = pd.read_csv(f, dtype=DType.OBJECT, quotechar="'")
        return ItemData(df)
