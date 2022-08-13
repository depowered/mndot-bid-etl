from typing import Callable
import pandas as pd
from mndot_bid_etl.extract.abstract import Abstract


def get_column_names_containing_string(
    df: pd.DataFrame, search_strings: list[str]
) -> list[str]:
    drop_columns = []
    for column_name in df.columns.to_list():
        for substring in search_strings:
            if substring in column_name:
                drop_columns.append(column_name)
    return drop_columns


def rename_bid_columns(column_name: str) -> str:
    match column_name:
        case "ItemNumber":
            return "item_id"
        case "Quantity":
            return column_name.lower()
        case other:
            return column_name.split(" ")[0].lower()


def format_item_id(id: str) -> str:
    return id[:4] + "." + id[4:]


def format_quantity(quantity: str) -> float:
    return float(quantity.strip())


def format_price(price: str) -> int:
    cleaned_str = price.strip().replace("$", "").replace(",", "")
    return int(float(cleaned_str) * 100)


def get_formattted_df(df: pd.DataFrame) -> pd.DataFrame:
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


def get_melted_df(df: pd.DataFrame) -> pd.DataFrame:
    return df.melt(
        id_vars=["item_id", "quantity"], var_name="bidder_id", value_name="unit_price"
    )


def get_transformed_bid_df(abstract: Abstract) -> pd.DataFrame:
    bid_df_raw = abstract.bid_df.copy()

    # Drop unnecessary columns
    drop_column_names_containing = [
        "ContractId",
        "SectionDescription",
        "LineNumber",
        "ItemDescription",
        "UnitPrice",
        "UnitName",
        "Ext",
    ]
    columns_to_drop = get_column_names_containing_string(
        bid_df_raw, drop_column_names_containing
    )
    bid_df_dropped = bid_df_raw.drop(columns=columns_to_drop)

    # Rename remaining columns
    bid_df_renamed = bid_df_dropped.rename(columns=rename_bid_columns)

    # Format and cast values
    bid_df_formatted = get_formattted_df(bid_df_renamed)

    # Reshape the dataframe with melt
    bid_df_melted = get_melted_df(bid_df_formatted)

    # Append contract_id and is_winning_bid columns
    bid_df_final = bid_df_melted.copy()
    bid_df_final["contract_id"] = abstract.contract_id
    bid_df_final["is_winning_bid"] = (
        bid_df_final["bidder_id"] == abstract.winning_bidder_id
    )

    return bid_df_final
