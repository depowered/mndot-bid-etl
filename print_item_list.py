from pathlib import Path
from mndot_bid_etl.transform.item_list import generate_item_list


item_list_2016_csv = Path("./mndot_bid_etl/data/csv/item_list_2016.csv").resolve()
item_list_2018_csv = Path("./mndot_bid_etl/data/csv/item_list_2018.csv").resolve()
item_list_2020_csv = Path("./mndot_bid_etl/data/csv/item_list_2020.csv").resolve()

item_list = generate_item_list(
    item_list_2016_csv, item_list_2018_csv, item_list_2020_csv
)


long_description_2020 = item_list.item_2020_df["long_description"].to_list()
for desc in long_description_2020:
    print(desc)
