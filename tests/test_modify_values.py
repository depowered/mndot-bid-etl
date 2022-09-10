from mndot_bid_etl.transform.recipes.bid import (
    format_item_id,
    format_long_description,
    format_price,
    format_quantity,
)
from mndot_bid_etl.transform.transformation import ModifyValues

from tests import test_abstract


def test_modify_values_on_bid_df() -> None:
    df = test_abstract.bid_df.copy()

    fuzzy_modify_map = {
        "ItemNumber": format_item_id,
        "ItemDescription": format_long_description,
        "Quantity": format_quantity,
        "(Unit Price)": format_price,
    }

    modify_values = ModifyValues(fuzzy_modify_map)
    modified_df = modify_values.apply(df)

    # Check that values were modified successfully
    assert modified_df.at[0, "ItemNumber"] == "2011.601/01000"
    assert modified_df.at[0, "ItemDescription"] == "AS BUILT"
    assert modified_df.at[0, "Quantity"] == 1.0
    assert modified_df.at[0, "Engineers (Unit Price)"] == 15_000_00

    # Check that an unspecified column values were unchanged
    assert (
        df["0000198793 (Extension)  "].to_list()
        == modified_df["0000198793 (Extension)  "].to_list()
    )
