import pandas as pd


def _generate_in_spec_year_df(df: pd.DataFrame) -> pd.DataFrame:
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


def transform_spec_year_matrix(
    df_2016: pd.DataFrame, df_2018: pd.DataFrame, df_2020: pd.DataFrame
) -> pd.DataFrame:

    in_2016 = _generate_in_spec_year_df(df_2016)
    in_2018 = _generate_in_spec_year_df(df_2018)
    in_2020 = _generate_in_spec_year_df(df_2020)

    spec_year_matrix = in_2016.join(other=[in_2018, in_2020], how="outer").fillna(
        value=False
    )

    return spec_year_matrix
