from typing import Callable
import pandas as pd

# ---------- Filter Column Functions ----------
def generate_filter_bid_column_list(df: pd.DataFrame) -> list[str]:
    # Add static column names
    filter_columns = ["ItemNumber", "Quantity"]

    # Add dynamic column names containing "(Unit Price)"
    substring = "(Unit Price)"
    df_columns = df.columns.to_list()
    dynamic_columns = [column for column in df_columns if substring in column]
    filter_columns += dynamic_columns

    return filter_columns


def filter_bid_columns(df: pd.DataFrame) -> pd.DataFrame:
    filter_columns = generate_filter_bid_column_list(df)
    return df.filter(items=filter_columns, axis="columns")


# ---------- Rename Functions ----------
def strip_bidder_id_column_names(column: str) -> str:
    return column.split(" ")[0].lower()


def generate_rename_column_mapper(df: pd.DataFrame) -> dict[str, str]:
    mapper = {}
    for column in df.columns.to_list():
        match column:
            case "ItemNumber":
                mapper[column] = "item_id"
            case "Quantity":
                mapper[column] = "quantity"
            case other:
                mapper[column] = strip_bidder_id_column_names(column)
    return mapper


def rename_bid_columns(df: pd.DataFrame) -> pd.DataFrame:
    mapper = generate_rename_column_mapper(df)
    return df.rename(columns=mapper)


# ---------- Format Functions ----------
def format_item_id(id: str) -> str:
    return id[:4] + "." + id[4:]


def format_quantity(quantity: str) -> float:
    return float(quantity.strip())


def format_price(price: str) -> int:
    cleaned_str = price.strip().replace("$", "").replace(",", "")
    return int(float(cleaned_str) * 100)


def format_bid_values(df: pd.DataFrame) -> pd.DataFrame:
    formatted_df = pd.DataFrame()
    for column_name in df.columns.to_list():
        format_function: Callable
        match column_name:
            case "item_id":
                format_function = format_item_id
            case "quantity":
                format_function = format_quantity
            case other:
                format_function = format_price
        formatted_df[column_name] = df[column_name].apply(format_function)
    return formatted_df


# ---------- Reshape Functions ----------
def melt_bid_df(df: pd.DataFrame) -> pd.DataFrame:
    return df.melt(
        id_vars=["item_id", "quantity"], var_name="bidder_id", value_name="unit_price"
    )


# ---------- Append Functions ----------
def assign_contract_id(df: pd.DataFrame, contract_id: str) -> pd.DataFrame:
    return df.assign(contract_id=contract_id)


# ---------- Transform Pipeline ----------
def transform_bid_df(df: pd.DataFrame, contract_id: str) -> pd.DataFrame:
    return (
        df.pipe(filter_bid_columns)
        .pipe(rename_bid_columns)
        .pipe(format_bid_values)
        .pipe(melt_bid_df)
        .pipe(assign_contract_id, contract_id)
    )
