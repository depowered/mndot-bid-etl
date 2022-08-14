import pandas as pd
from mndot_bid_etl.extract.abstract import Abstract


def rename_contract_columns(df: pd.DataFrame, mapper: dict[str, str]) -> pd.DataFrame:
    return df.rename(columns=mapper)


def assign_winning_bidder_id(df: pd.DataFrame, winning_bidder_id: str) -> pd.DataFrame:
    return df.assign(winning_bidder_id=winning_bidder_id)


# TODO: Implement an method for determining the spec year from the abstract content
def assign_spec_year(df: pd.DataFrame, spec_year: int) -> pd.DataFrame:
    return df.assign(spec_year=spec_year)


def transform_contract_df(abstract: Abstract) -> pd.DataFrame:
    mapper = {
        "Letting Date": "letting_date",
        "Job Description": "description",
        "Contract Id": "id",
        "SP Number": "sp_number",
        "District": "district",
        "County": "county",
    }
    df = abstract.contract_df

    return (
        df.pipe(rename_contract_columns, mapper=mapper)
        .pipe(assign_winning_bidder_id, winning_bidder_id=abstract.winning_bidder_id)
        .pipe(assign_spec_year, spec_year=2001)
    )
