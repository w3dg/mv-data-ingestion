import os
from typing import Optional
import json
import requests as r
from utils.file_utils import save_json, load_json


def fetchCryptoPanic() -> Optional[dict]:
    CRYPTOPANIC_API_KEY = os.getenv("CRYPTOPANIC_API_KEY")
    if CRYPTOPANIC_API_KEY is None:
        print("CryptoPanic API Key Not found in environment")
        return None
    CRYPTOPANIC_URL = (
        f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTOPANIC_API_KEY}"
    )
    # Uncomment the following lines to fetch from API
    # res = r.get(CRYPTOPANIC_URL)
    # if res.status_code != 200:
    #     print("Could not fetch CryptoPanic")
    #     return None
    # jsonresponse = res.json()
    # # Save to file
    # save_json("cryptopanic.json", jsonresponse)
    # return jsonresponse

    # Load from saved file instead
    contents = load_json("cryptopanic.json")
    return contents


def getCryptoPanicData():
    newsjson = fetchCryptoPanic()
    if newsjson is not None:
        print("cryptopanic data fetched")
        for post in newsjson.get("results", []):
            print(post["title"])
            print(post["description"])
            print()
