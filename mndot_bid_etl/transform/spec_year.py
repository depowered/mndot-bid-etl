import pandas as pd


# TODO: Use this somewhere
def determine_spec_year(
    transformed_abstract: TransformedAbstract, spec_year_matrix: SpecYearMatrix
) -> str:
    # Construct dataframe with compound_id (item_id + "_" + long_description) from the transformed bid_df
    df = pd.DataFrame(transformed_abstract.bid_df["compound_id"])

    # Merge the spec_year_matrix columns "is_in_2016", "is_in_2018", "is_in_2020"
    df_matrix = df.merge(
        spec_year_matrix, how="left", on="compound_id", suffixes=["", ""]
    )

    # Determine the year with the highest True count
    true_counts = (
        df_matrix[["is_in_2016", "is_in_2018", "is_in_2020"]].sum(axis=0).to_dict()
    )
    count_2016, count_2018, count_2020 = true_counts.values()

    if count_2020 >= count_2018:
        return "2020"
    elif count_2018 >= count_2016:
        return "2018"
    else:
        return "2016"
