import pandas as pd


def transform_item(df: pd.DataFrame) -> pd.DataFrame:

    out_df = pd.DataFrame()

    out_df["spec_year"] = "20" + df["Spec Year"]
    out_df["spec_code"] = df["Item Number"].str.slice(0, 4)
    out_df["unit_code"] = df["Item Number"].str.slice(5, 8)
    out_df["item_code"] = df["Item Number"].str.slice(9, 14)
    out_df["short_description"] = (
        df["Short Description"].str.strip().str.replace(";", ",")
    )
    out_df["long_description"] = (
        df["Long Description"].str.strip().str.replace(";", ",")
    )
    out_df["unit"] = df["Plan Unit Description"].str.strip()
    out_df["unit_abbreviation"] = df["Unit Name"].str.strip().str.replace(" ", "")

    return out_df
