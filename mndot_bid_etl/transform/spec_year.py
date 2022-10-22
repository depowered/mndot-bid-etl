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
