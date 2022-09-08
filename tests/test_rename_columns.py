from mndot_bid_etl.transform.transformation import RenaneColumns

from tests import test_abstract, test_items


def test_rename_columns_on_bid_df() -> None:
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


def test_rename_columns_on_bidder_df() -> None:
    df = test_abstract.bidder_df.copy()

    rename_map = {"Bidder Number": lambda _: "id", "Bidder Name": lambda _: "name"}

    rename_columns = RenaneColumns(rename_map)
    renamed_df = rename_columns.apply(df)
    result_column_names = renamed_df.columns.to_list()

    expected_column_names = ["id", "name", "Bidder Amount"]

    assert result_column_names == expected_column_names


def test_rename_columns_on_contract_df() -> None:
    df = test_abstract.contract_df.copy()

    rename_map = {
        "Letting Date": lambda _: "letting_date",
        "Job Description": lambda _: "description",
        "Contract Id": lambda _: "id",
        "SP Number": lambda _: "sp_number",
        "District": lambda _: "district",
        "County": lambda _: "county",
    }

    rename_columns = RenaneColumns(rename_map)
    renamed_df = rename_columns.apply(df)
    result_column_names = renamed_df.columns.to_list()

    expected_column_names = [
        "letting_date",
        "description",
        "id",
        "sp_number",
        "district",
        "county",
    ]

    assert result_column_names == expected_column_names


def test_rename_columns_on_item_df() -> None:
    df = test_items.copy()

    rename_map = {
        "Item Number": lambda _: "id",
        "Short Description": lambda _: "description",
        "Long Description": lambda _: "long_description",
        "Unit Name": lambda _: "unit",
        "Plan Unit Description": lambda _: "unit_description",
        "Spec Year": lambda _: "spec_year",
    }

    rename_columns = RenaneColumns(rename_map)
    renamed_df = rename_columns.apply(df)
    result_column_names = renamed_df.columns.to_list()

    expected_column_names = [
        "id",
        "description",
        "long_description",
        "unit",
        "unit_description",
        "spec_year",
        "Unnamed: 6",
    ]

    assert result_column_names == expected_column_names


def test_rename_columns_with_no_matches() -> None:
    df = test_items.copy()

    rename_map = {"NonMatchingText1": lambda _: None}

    rename_columns = RenaneColumns(rename_map)
    renamed_df = rename_columns.apply(df)
    result_column_names = renamed_df.columns.to_list()

    expected_column_names = [
        "Item Number",
        "Short Description",
        "Long Description",
        "Unit Name",
        "Plan Unit Description",
        "Spec Year",
        "Unnamed: 6",
    ]

    assert result_column_names == expected_column_names
