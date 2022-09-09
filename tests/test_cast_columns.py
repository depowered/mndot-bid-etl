from mndot_bid_etl.transform.transformation import CastColumns, DType

from tests import test_abstract


def test_cast_columns_on_contract_df() -> None:
    df = test_abstract.contract_df.copy()

    fuzzy_dtype_map = {"Letting Date": DType.DATE}

    cast_columns = CastColumns(fuzzy_dtype_map)
    casted_df = cast_columns.apply(df)
    resulting_dtype = casted_df["Letting Date"].dtype

    expected_dtype = "datetime64[ns]"

    assert resulting_dtype == expected_dtype


def test_cast_columns_with_no_matches() -> None:
    df = test_abstract.contract_df.copy()

    fuzzy_dtype_map = {"NonMatchingText1": DType.DATE}

    cast_columns = CastColumns(fuzzy_dtype_map)
    casted_df = cast_columns.apply(df)
    resulting_dtype = casted_df["Letting Date"].dtype

    expected_dtype = "object"

    assert resulting_dtype == expected_dtype
