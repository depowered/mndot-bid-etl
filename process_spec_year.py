from pathlib import Path

from mndot_bid_etl.reader.abstract import create_abstract_data_from_csv
from mndot_bid_etl.reader.item import create_item_data_from_csv
from mndot_bid_etl.transform import item, spec_year


def process_spec_year(year: int) -> None:

    # Load raw item data
    item_data_2016 = create_item_data_from_csv(
        Path("./data/csv/item_list_2016.csv").resolve()
    )
    item_data_2020 = create_item_data_from_csv(
        Path("./data/csv/item_list_2020.csv").resolve()
    )
    item_data_2018 = create_item_data_from_csv(
        Path("./data/csv/item_list_2018.csv").resolve()
    )

    # Transform item dfs
    df_2016 = item.transform_item(item_data_2016.df)
    df_2018 = item.transform_item(item_data_2018.df)
    df_2020 = item.transform_item(item_data_2020.df)

    spec_year_matrix = spec_year.create_spec_year_matrix([df_2016, df_2018, df_2020])
    print("Spec year matrix created")

    # Create list of csv paths
    csv_dir = Path(f"./data/csv/{str(year)}").resolve()
    csvs = sorted(csv_dir.rglob("*.csv"))

    with open(f"./data/csv/{year}.txt", "w") as log:
        for csv in csvs:
            try:
                abstract_data = create_abstract_data_from_csv(csv)
                print(f"Processing {abstract_data.contract_id}")
                estimated_spec_year = spec_year.determine_contract_spec_year(
                    spec_year_matrix, abstract_data.bid_df
                )

                log.write(
                    f"Contract id: {abstract_data.contract_id}, Spec Year: {estimated_spec_year}\n"
                )
            except:
                log.write(f"Exception occured processing path: {csv}\n")


if __name__ == "__main__":
    process_spec_year(2021)
