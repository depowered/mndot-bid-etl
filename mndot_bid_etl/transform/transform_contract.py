import pandas as pd


def rename_contract_columns(df: pd.DataFrame) -> pd.DataFrame:
    mapper = {
        "Letting Date": "letting_date",
        "Job Description": "description",
        "Contract Id": "id",
        "SP Number": "sp_number",
        "District": "district",
        "County": "county",
    }
    return df.rename(columns=mapper)


def assign_winning_bidder_id(df: pd.DataFrame, winning_bidder_id: str) -> pd.DataFrame:
    return df.assign(winning_bidder_id=winning_bidder_id)


def cast_contract_astype(df: pd.DataFrame) -> pd.DataFrame:
    dtype = {"Letting Date": "datetime64[ns]"}
    return df.astype(dtype)


# TODO: Implement an method for determining the spec year from the abstract content
def assign_spec_year(df: pd.DataFrame, spec_year: str) -> pd.DataFrame:
    return df.assign(spec_year=spec_year)


def transform_contract_df(
    df: pd.DataFrame, winning_bidder_id: str, spec_year: str
) -> pd.DataFrame:

    return (
        df.pipe(cast_contract_astype)
        .pipe(rename_contract_columns)
        .pipe(assign_winning_bidder_id, winning_bidder_id=winning_bidder_id)
        .pipe(assign_spec_year, spec_year=spec_year)
    )
