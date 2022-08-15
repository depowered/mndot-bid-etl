from pathlib import Path
import requests


def fetch_item_list_csv(year: int) -> str:
    url = "https://transport.dot.state.mn.us/Reference/refItem.aspx"

    # The payload below was copied from the post request after navigating to the target page manually
    payload = {
        "__EVENTTARGET": "ctl00$MainContent$LinkButton1",
        "__EVENTARGUMENT": "",
        "__VIEWSTATE": "/wEPDwULLTIwMDA0NDA2NDMPZBYCZg9kFgICBQ9kFgYCAQ8PFgIeBFRleHQFLk1uRE9UIFN0YW5kYXJkIFNwZWNpZmljYXRpb25zIEZvciBDb25zdHJ1Y3Rpb25kZAIDDw8WBh8ABRxBQVNIVE9XYXJlIFByb2plY3QgSXRlbSBMaXN0HglGb3JlQ29sb3IKIx4EXyFTQgIEZGQCBw9kFgoCCw8PFgIeB1Zpc2libGVoZGQCDQ8PFgQeB0VuYWJsZWRoHwNoZGQCDw88KwARAwAPFgIeClNob3dGb290ZXJnZAEQFgAWABYADBQrAABkAhEPDxYCHwNoZGQCEw8QDxYCHwNoZGQWAWZkGAEFG2N0bDAwJE1haW5Db250ZW50JGd2UmVmSXRlbQ9nZFZ2Tkr2GBiyGu0BSbGsRRcBrJEek75yTAqWIU+udILr",
        "__VIEWSTATEGENERATOR": "115E9492",
        "__EVENTVALIDATION": "/wEdAAlQLBtT5HVTDC4gDKSIpUwT6XUEVaVArTknM/AIWiCmfySb5Jo7EHUVWCUvRhlv/0AwqNmbkwlGkLb4J9MVp7aV2ihq8vT00whimHTWykdtvW4wVUxmqwHa7Jm3PxNshdFi6UFpibrPn/7jjn5BJwDecJsAD0Rh1DuNbxILM//pi4Sh4NK+piAusjW3zkSES+tAvW/ivrFDJbxZdS8szCbf3qMj1DXo0Q3R5WedzM+BZw==",
        "ctl00$MainContent$txtDescr": "",
        "ctl00$MainContent$rdSpecYear": str(year)[2:],  # "2018" -> "18"
    }

    try:
        r = requests.post(url=url, data=payload)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise e

    return r.text


def download_item_list_csv(year: int, download_dir: Path) -> None:
    file_name = f"item_list_{year}.csv"
    file_path = download_dir / file_name

    # Check if file already exists
    if file_path.is_file():
        return

    csv_text = fetch_item_list_csv(year)
    with open(file_path, "w") as f:
        f.write(csv_text)
