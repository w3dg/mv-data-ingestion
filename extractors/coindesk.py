import os
from typing import Optional

import pandas as pd
import requests as r
from fastfeedparser import parse as fastfeedparse

from utils.file_utils import load_json, save_json


def fetchCoinDeskNews() -> Optional[list[dict]]:
    COIN_DESK_URL = "https://www.coindesk.com/arc/outboundfeeds/rss"
    res = r.get(COIN_DESK_URL)
    if res.status_code != 200:
        print("Could not fetch CoinDesk")
        return None
    myfeed = fastfeedparse(res.text)
    feedentries = myfeed.get("entries", [])
    extracted_entries = []
    for entry in feedentries:
        extracted_entry = {
            "id": entry.get("id"),
            "title": entry.get("title"),
            "link": entry.get("link"),
            "description": entry.get("description"),
            "published": entry.get("published"),
        }
        extracted_entries.append(extracted_entry)
    save_json("coindesk.json", extracted_entries)
    return extracted_entries


def getCoinDesk() -> Optional[pd.DataFrame]:
    cdnews = None
    cddf = None
    if os.getenv("USE_CACHE") == 1:
        cdnews: Optional[list[dict]] = load_json("coindesk.json")
    else:
        cdnews = fetchCoinDeskNews()

    if cdnews is not None:
        cddf = pd.DataFrame(cdnews)
        print(f"{len(cddf)} items from coindesk fetched")

    return cddf
