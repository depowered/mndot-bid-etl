from mndot_bid_etl.transform.transformation import FilterColumns

from tests import test_abstract, test_items


def test_filter_columns_on_bid_df() -> None:
    df = test_abstract.bid_df.copy()

    filter_list = ["ItemNumber", "ItemDescription", "Quantity", "(Unit Price)"]

    filter_columns = FilterColumns(filter_list)
    filtered_df = filter_columns.apply(df)
    result_columns = filtered_df.columns.to_list()

    expected_columns = [
        "ItemNumber",
        "ItemDescription",
        "Quantity",
        "Engineers (Unit Price)",
        "0000198793 (Unit Price) ",
        "0000210000 (Unit Price) ",
        "0000207897 (Unit Price) ",
    ]

    assert result_columns == expected_columns


def test_filter_columns_on_bidder_df() -> None:
    df = test_abstract.bidder_df.copy()

    filter_list = ["Bidder Number", "Bidder Name"]

    filter_columns = FilterColumns(filter_list)
    filtered_df = filter_columns.apply(df)
    result_columns = filtered_df.columns.to_list()

    expected_columns = ["Bidder Number", "Bidder Name"]

    assert result_columns == expected_columns


def test_filter_columns_on_item_df() -> None:
    df = test_items.copy()

    filter_list = [
        "Item Number",
        "Short Description",
        "Long Description",
        "Unit Name",
        "Plan Unit Description",
        "Spec Year",
    ]

    filter_columns = FilterColumns(filter_list)
    filtered_df = filter_columns.apply(df)
    result_columns = filtered_df.columns.to_list()

    expected_columns = [
        "Item Number",
        "Short Description",
        "Long Description",
        "Unit Name",
        "Plan Unit Description",
        "Spec Year",
    ]

    assert result_columns == expected_columns


def test_filter_columns_with_no_matches() -> None:
    df = test_abstract.bidder_df.copy()

    filter_list = ["NonMatchingText1", "NonMatchingText2"]

    filter_columns = FilterColumns(filter_list)
    filtered_df = filter_columns.apply(df)
    result_columns = filtered_df.columns.to_list()

    expected_columns = []

    assert result_columns == expected_columns
