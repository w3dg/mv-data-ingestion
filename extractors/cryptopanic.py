import os
from typing import Optional

import pandas as pd
import requests as r

from utils.file_utils import load_json, save_json


def fetchCryptoPanic() -> Optional[list[dict]]:
    CRYPTOPANIC_API_KEY = os.getenv("CRYPTOPANIC_API_KEY")
    if CRYPTOPANIC_API_KEY is None:
        print("CryptoPanic API Key Not found in environment")
        return None
    CRYPTOPANIC_URL = (
        f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTOPANIC_API_KEY}"
    )

    extracted_entries = []
    res = r.get(CRYPTOPANIC_URL)
    if res.status_code != 200:
        print("Could not fetch CryptoPanic")
        return None
    jsonresponse = res.json()

    results = jsonresponse.get("results", [])
    for entry in results:
        extracted_entry = {
            "id": entry.get("id"),
            "title": entry.get("title"),
            "description": entry.get("description"),
            "published_at": entry.get("published_at"),
        }
        extracted_entry["url"] = (
            f"https://cryptopanic.com/{entry.get('kind')}/{entry.get('id')}/{entry.get('slug')}"
        )

        extracted_entries.append(extracted_entry)

    save_json("cryptopanic.json", extracted_entries)
    return extracted_entries


def getCryptoPanicData() -> Optional[pd.DataFrame]:
    newsjson: Optional[list[dict]] = None
    cpdf: Optional[pd.Dataframe] = None

    if os.getenv("USE_CACHE") == 1:
        newsjson = load_json("cryptopanic.json")
    else:
        newsjson = fetchCryptoPanic()

    if newsjson is not None:
        cpdf = pd.DataFrame(newsjson)
        print(len(cpdf), "items fetched from cryptopanic")

    return cpdf
