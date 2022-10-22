import pandas as pd


def _generate_in_spec_year_df(df: pd.DataFrame) -> pd.DataFrame:
    """Generates a Dataframe with the following index structure and a spec year column filled with True.

    index: `{spec_code}_{unit_code}_{item_code}_{long_description}`
    index example: `2011_601_00003_CONSTRUCTION SURVEYING`
    """
    spec_year = df.at[0, "spec_year"]

    merged_id = (
        df["spec_code"]
        + "_"
        + df["unit_code"]
        + "_"
        + df["item_code"]
        + "_"
        + df["long_description"]
    )

    out_df = pd.DataFrame({"merged_id": merged_id, spec_year: True})
    return out_df.set_index("merged_id")


def create_spec_year_matrix(tranformed_item_dfs: list[pd.DataFrame]) -> pd.DataFrame:

    spec_year_dfs = [_generate_in_spec_year_df(df) for df in tranformed_item_dfs]

    spec_year_matrix = (
        spec_year_dfs[0].join(other=spec_year_dfs[1:], how="outer").fillna(value=False)
    )

    return spec_year_matrix


def determine_contract_spec_year(
    spec_year_matrix: pd.DataFrame, raw_bid_df: pd.DataFrame
) -> str:
    def format_long_description(long_description: str) -> str:
        return long_description.strip().replace("''", '"')

    # Create merged_id indexed DataFrame from raw_bid_df
    contract_items_df = pd.DataFrame()
    contract_items_df["merged_id"] = (
        raw_bid_df["ItemNumber"].str.slice(0, 4)
        + "_"
        + raw_bid_df["ItemNumber"].str.slice(4, 7)
        + "_"
        + raw_bid_df["ItemNumber"].str.slice(8)
        + "_"
        + raw_bid_df["ItemDescription"].apply(format_long_description)
    )
    contract_items_df.set_index("merged_id", inplace=True)

    # Merge with spec_year_matrix
    merged_df = contract_items_df.merge(spec_year_matrix, how="left", on="merged_id")

    # Estimate spec year
    contract_item_count = raw_bid_df.shape[0]
    matches = {"item_count": contract_item_count}

    for spec_year in merged_df.columns.to_list():
        item_in_spec_year_count = merged_df[spec_year].value_counts()[True]
        matches[f"{spec_year}_matches"] = item_in_spec_year_count
        if contract_item_count == item_in_spec_year_count:
            return spec_year

    return str(matches)
