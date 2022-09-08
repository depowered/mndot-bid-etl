from pathlib import Path

from mndot_bid_etl.transform.abstract import Abstract, read_abstract_csv

# Setup test abstract data
csv_file = Path("./tests/data/test_abstract.csv").resolve()
test_abstract = read_abstract_csv(csv_file)
