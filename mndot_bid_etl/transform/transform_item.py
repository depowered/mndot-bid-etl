import pandas as pd


# ---------- Filter Column Functions ----------
def filter_item_columns(df: pd.DataFrame) -> pd.DataFrame:
    filter_columns = [
        "Item Number",
        "Short Description",
        "Long Description",
        "Unit Name",
        "Plan Unit Description",
        "Spec Year",
    ]
    return df.filter(items=filter_columns, axis="columns")


# ---------- Rename Functions ----------
def rename_item_columns(df: pd.DataFrame) -> pd.DataFrame:
    mapper = {
        "Item Number": "id",
        "Short Description": "description",
        "Long Description": "long_description",
        "Unit Name": "unit",
        "Plan Unit Description": "unit_description",
        "Spec Year": "spec_year",
    }
    return df.rename(columns=mapper)


# ---------- Format Functions ----------
def format_item_values(df: pd.DataFrame) -> pd.DataFrame:
    formatted_df = df.copy()
    formatted_df["spec_year"] = (
        formatted_df["spec_year"].apply(lambda x: "20" + x).astype("string")
    )
    # formatted_df = formatted_df.applymap(str.strip)
    for column in formatted_df.columns.to_list():
        formatted_df[column] = formatted_df[column].str.strip()
    return formatted_df


# ---------- Format Functions ----------
def transform_item_df(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.pipe(filter_item_columns).pipe(rename_item_columns).pipe(format_item_values)
    )
