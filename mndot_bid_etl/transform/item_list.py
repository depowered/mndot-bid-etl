from pathlib import Path
from dataclasses import dataclass
import pandas as pd

from mndot_bid_etl.transform.functional.transform_item import transform_item_df


@dataclass
class ItemList:
    item_2016_df: pd.DataFrame
    item_2018_df: pd.DataFrame
    item_2020_df: pd.DataFrame

    def __post_init__(self) -> None:
        self.compound_id_matrix = self._generate_compound_id_matrix()
        self.unique_2020_compound_ids = self._generate_unique_compound_ids_set(
            is_in_2016=False, is_in_2018=False, is_in_2020=True
        )
        self.unique_2018_compound_ids = self._generate_unique_compound_ids_set(
            is_in_2016=False, is_in_2018=True, is_in_2020=False
        )
        self.unique_2016_compound_ids = self._generate_unique_compound_ids_set(
            is_in_2016=True, is_in_2018=False, is_in_2020=False
        )

    def _generate_compound_ids(self, df: pd.DataFrame) -> pd.Series:
        return df["id"] + "_" + df["long_description"]

    def _generate_compound_id_matrix(self) -> pd.DataFrame:
        compound_id_2020 = self._generate_compound_ids(self.item_2020_df)
        compound_id_2020_df = pd.DataFrame(index=compound_id_2020).assign(
            is_in_2020=True
        )
        compound_id_2018 = self._generate_compound_ids(self.item_2018_df)
        compound_id_2018_df = pd.DataFrame(index=compound_id_2018).assign(
            is_in_2018=True
        )
        compound_id_2016 = self._generate_compound_ids(self.item_2016_df)
        compound_id_2016_df = pd.DataFrame(index=compound_id_2016).assign(
            is_in_2016=True
        )
        compound_id_matrix = compound_id_2016_df.join(
            other=[compound_id_2018_df, compound_id_2020_df], how="outer"
        )
        compound_id_matrix.fillna(value=False, inplace=True)
        return compound_id_matrix

    def _generate_unique_compound_ids_set(
        self, is_in_2016: bool, is_in_2018: bool, is_in_2020: bool
    ) -> set[str]:
        compound_ids_matrix = self._generate_compound_id_matrix()

        statement = f"is_in_2016 == {is_in_2016} & is_in_2018 == {is_in_2018} & is_in_2020 == {is_in_2020}"
        unique_compound_ids = set(compound_ids_matrix.query(statement).index.to_list())

        return unique_compound_ids


def read_item_list_csv(csv_file: Path) -> pd.DataFrame:
    with open(csv_file, "r") as f:
        return pd.read_csv(f, dtype="string", quotechar="'")


def generate_item_list(
    item_list_2016_csv: Path, item_list_2018_csv: Path, item_list_2020_csv: Path
) -> ItemList:
    return ItemList(
        item_2016_df=transform_item_df(read_item_list_csv(item_list_2016_csv)),
        item_2018_df=transform_item_df(read_item_list_csv(item_list_2018_csv)),
        item_2020_df=transform_item_df(read_item_list_csv(item_list_2020_csv)),
    )
