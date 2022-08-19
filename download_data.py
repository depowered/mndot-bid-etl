from pathlib import Path
import requests

from mndot_bid_etl.extract.abstract_csv import download_abstract_csv, get_contract_ids
from mndot_bid_etl.extract.item_list_csv import download_item_list_csv


DOWNLOAD_DIR = Path("./data/csv").resolve()
ABSTRACT_CSV_YEARS = [2022, 2020, 2019, 2018]
ITEM_LIST_YEARS = [2016, 2018, 2020]


def main() -> None:
    # Download all abstract csvs for each year
    for year in ABSTRACT_CSV_YEARS:
        print(f"----- Downloading Abstract CSVs for {year} -----")

        abstract_year_dir = DOWNLOAD_DIR / str(year)
        contract_ids = get_contract_ids(year)
        for idx, id in enumerate(contract_ids):
            print(f"Downloading {id}.csv ({idx + 1} of {len(contract_ids)})")
            try:
                download_abstract_csv(contract_id=id, download_dir=abstract_year_dir)
            except requests.exceptions.RequestException as e:
                print(e)
                continue

    # Download all item lists
    for year in ITEM_LIST_YEARS:
        print(f"----- Downloading Item List CSV for {year} -----")

        try:
            download_item_list_csv(year, DOWNLOAD_DIR)
        except requests.exceptions.RequestException as e:
            print(e)
            continue


if __name__ == "__main__":
    main()
