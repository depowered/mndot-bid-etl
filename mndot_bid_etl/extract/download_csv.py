from pathlib import Path
import requests
from fetch_contract_ids import get_contract_ids

csv_folder = Path("../data/csv")
CSV_DOWNLOAD_BASE_URL = (
    "http://transport.dot.state.mn.us/PostLetting/abstractCSV.aspx?ContractId="
)


def download_csv(contract_ids: list[str], save_path: Path) -> None:
    for idx, id in enumerate(contract_ids):
        # If file exists, don't re-download
        csv_file: Path = save_path / f"{id}.csv"
        if csv_file.is_file():
            continue

        print(f"Downloading {id}.csv ({idx + 1} of {len(contract_ids)})")
        try:
            url = CSV_DOWNLOAD_BASE_URL + id
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(e)
            continue

        with open(csv_file, "w") as f:
            f.write(r.text)


def main() -> None:
    years = [2022, 2021, 2020, 2019, 2018]
    for year in years:
        print(f"Downloading abstract CSVs for {year}")
        contract_ids = get_contract_ids(year)
        save_path = csv_folder / str(year)
        download_csv(contract_ids, save_path)


if __name__ == "__main__":
    main()
