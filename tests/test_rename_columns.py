from mndot_bid_etl.transform.transformation import RenaneColumns

from tests import test_abstract


def test_rename_columns() -> None:
    df = test_abstract.bid_df.copy()

    rename_map = {
        "ItemNumber": lambda _: "item_id",
        "ItemDescription": lambda _: "long_description",
        "Quantity": lambda x: x.lower(),
        "(Unit Price)": lambda x: x.strip().split(" ")[0].lower(),
    }

    rename_columns = RenaneColumns(rename_map)
    renamed_df = rename_columns.apply(df)
    result_column_names = renamed_df.columns.to_list()

    expected_column_names = [
        "ContractId",
        "SectionDescription",
        "LineNumber",
        "item_id",
        "long_description",
        "UnitPrice",
        "quantity",
        "UnitName",
        "engineers",
        "Engineers (Extended Amount)",
        "0000198793",
        "0000198793 (Extension)  ",
        "0000210000",
        "0000210000 (Extension)  ",
        "0000207897",
        "0000207897 (Extension)  ",
    ]

    assert result_column_names == expected_column_names
