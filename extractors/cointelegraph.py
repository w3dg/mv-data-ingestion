import json
from typing import Optional
import requests as r
from fastfeedparser import FastFeedParserDict, parse as fastfeedparse

from utils.file_utils import save_json


def fetchCoinTelegraphNews() -> Optional[FastFeedParserDict]:
    COIN_TELEGRAPH_URL = "https://cointelegraph.com/rss"
    res = r.get(COIN_TELEGRAPH_URL)
    if res.status_code != 200:
        print("Could not fetch Coin telegraph")
        return None
    myfeed = fastfeedparse(res.text)
    feedjson = json.dumps(myfeed)
    save_json("cointelegraph.json", feedjson)
    return myfeed


def getCoinTelegraph():
    ctnews = fetchCoinTelegraphNews()
    if ctnews is not None:
        news_entries = ctnews["entries"]
        print(f"{len(news_entries)} items from coin telegraph fetched")
