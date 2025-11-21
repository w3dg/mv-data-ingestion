import json
from typing import Optional
import requests as r
from fastfeedparser import FastFeedParserDict, parse as fastfeedparse

from utils.file_utils import save_json


def fetchCoinDeskNews() -> Optional[FastFeedParserDict]:
    COIN_DESK_URL = "https://www.coindesk.com/arc/outboundfeeds/rss"
    res = r.get(COIN_DESK_URL)
    if res.status_code != 200:
        print("Could not fetch CoinDesk")
        return None
    myfeed = fastfeedparse(res.text)
    feedjson = json.dumps(myfeed)
    save_json("coindesk.json", feedjson)
    return myfeed


def getCoinDesk():
    ctnews = fetchCoinDeskNews()
    if ctnews is not None:
        news_entries = ctnews["entries"]
        print(f"{len(news_entries)} items from coindesk fetched")
