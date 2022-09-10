from pathlib import Path

from mndot_bid_etl.reader.abstract import create_abstract_data_from_csv
from mndot_bid_etl.reader.item import create_item_data_from_csv

# Setup test abstract data
test_abstract = create_abstract_data_from_csv(
    Path("./tests/data/test_abstract.csv").resolve()
)

# Setup test items data
test_items = create_item_data_from_csv(Path("./tests/data/test_items.csv").resolve())
