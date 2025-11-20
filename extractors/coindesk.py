from typing import Optional
import requests as r
from fastfeedparser import FastFeedParserDict, parse as fastfeedparse


def fetchCoinDeskNews() -> Optional[FastFeedParserDict]:
    COIN_DESK_URL = "https://www.coindesk.com/arc/outboundfeeds/rss"
    res = r.get(COIN_DESK_URL)
    if res.status_code != 200:
        print("Could not fetch CoinDesk")
        return None
    myfeed = fastfeedparse(res.text)
    return myfeed


def getCoinDesk():
    ctnews = fetchCoinDeskNews()
    if ctnews is not None:
        news_entries = ctnews["entries"]
        print(f"{len(news_entries)} items from coindesk fetched")
