import os
from typing import Optional
import json
import requests as r
from utils.file_utils import save_json, load_json


def fetchNewsDataIO() -> Optional[dict]:
    NEWSDATA_API_KEY = os.getenv("NEWSDATA_API_KEY")
    if NEWSDATA_API_KEY is None:
        print("NewsData API Key Not found in environment")
        return None
    NEWSDATA_URL = f"https://newsdata.io/api/1/crypto?apikey={NEWSDATA_API_KEY}"
    # res = r.get(NEWSDATA_URL)
    # if res.status_code != 200:
    #     print("Could not fetch NewsData")
    #     return None
    # jsonresponse = res.json()
    # print(jsonresponse)
    # save_json("newsdata.json", jsonresponse)
    # return jsonresponse

    contents = load_json("newsdata.json")
    return contents


def getNewsData():
    newsjson = fetchNewsDataIO()
    if newsjson is not None:
        print("newsdata.io fetched")
        for r in newsjson["results"]:
            print(r["title"])
            print(r["description"])
            print(r["article_id"])
            print()
