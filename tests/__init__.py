from pathlib import Path

from mndot_bid_etl.transform.abstract import read_abstract_csv
from mndot_bid_etl.transform.item_list import read_item_list_csv

# Setup test abstract data
test_abstract = read_abstract_csv(Path("./tests/data/test_abstract.csv").resolve())

# Setup test items data
test_items = read_item_list_csv(Path("./tests/data/test_items.csv").resolve())
