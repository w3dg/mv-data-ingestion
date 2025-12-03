import os
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

import pandas as pd
import requests as r

from utils.file_utils import load_json, save_json

subreddits = ["CryptoCurrency", "ethfinance", "CryptoMarkets", "ethereum"]
# r/ethereum has daily discussion posts


def fetchSubreddit(subreddit, limit=10) -> list[dict]:
    headers = {
        "origin": "https://reddit.com",
        "User-Agent": os.getenv(
            "REDDIT_USER_AGENT",
            "python:Volaility-Sentiment:v0.1 (by /u/Several-Winter-2059/)",
        ),
    }
    url = f"https://cors-anywhere.com/https://reddit.com/r/{subreddit}/new.json"
    retries = 3
    posts = []

    while retries > 0:
        response = r.get(url, headers=headers)

        if response.status_code != 200:
            print("Failed to fetch data, will retry")
            print(f"Failed to fetch data from r/{subreddit}: {response.status_code}")
            if response.status_code == 403:
                print("Got response Forbidden from reddit, retrying")
            retries -= 1
            time.sleep(5)
        else:
            resjson = response.json()
            data = resjson.get("data", {})
            posts = data.get("children", [])
            print(f"Fetched {len(posts)} posts from reddit")
            break

    if retries == 0 and len(posts) == 0:
        print("Failed to get reddit data after 3 retries")
        return []

    return posts


def fetchRedditPosts(subreddits, limit=10) -> list[dict]:
    extracted_posts = []
    with ThreadPoolExecutor(max_workers=3) as executor:
        list_all_posts = (
            list(executor.map(fetchSubreddit, subreddits, len(subreddits) * [limit])),
        )[0]
        for posts in list_all_posts:
            extracted_posts.extend(posts)
    results = []
    for post in extracted_posts:
        post_data = post["data"]
        results.append(
            {
                "id": f"{post_data.get('subreddit_id')}-{post_data.get('id')}",
                "title": post_data.get("title"),
                "url": post_data.get("url"),
                "description": post_data.get("selftext"),
                "created_utc": str(post_data.get("created_utc")),
                "subreddit": post_data.get("subreddit"),
            }
        )
    save_json("reddit_data.json", results)
    return results


def getRedditData() -> Optional[pd.DataFrame]:
    rdtdf = None
    all_posts: Optional[list[dict]] = None

    if os.getenv("USE_CACHE") == 1:
        all_posts = load_json("reddit_data.json")
    else:
        all_posts = fetchRedditPosts(subreddits, limit=10)

    if all_posts is not None and len(all_posts) > 0:
        rdtdf = pd.DataFrame(all_posts)
        print("Reddit data fetched")
        print("Total posts fetched:", len(rdtdf))
    else:
        print("Could not fetch reddit data")

    return rdtdf
