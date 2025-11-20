import os
from typing import Optional
import json
import yfinance as yf
from utils.file_utils import save_json, load_json


def fetchYFinance() -> Optional[dict]:
    # List of crypto tickers to fetch data for
    crypto_tickers = ["BTC-USD", "ETH-USD", "ADA-USD", "SOL-USD", "DOT-USD"]

    # Uncomment the following lines to fetch from API
    # news_data = {}
    # for ticker in crypto_tickers:
    #     try:
    #         ticker_obj = yf.Ticker(ticker)
    #         news = ticker_obj.news
    #         info = ticker_obj.info
    #         news_data[ticker] = {"news": news, "info": info}
    #     except Exception as e:
    #         print(f"Error fetching data for {ticker}: {e}")
    #         news_data[ticker] = {"news": [], "info": {}}

    # # Save to file
    # save_json("yfinance.json", news_data)
    # return news_data

    # Load from saved file instead
    contents = load_json("yfinance.json")
    return contents


def getYFinanceData():
    newsjson = fetchYFinance()
    if newsjson is not None:
        print("yfinance data fetched")
        for ticker, data in newsjson.items():
            print(f"Ticker: {ticker}")
            print(f"News count: {len(data.get('news', []))}")
            for article in data.get("news", []):
                content = article.get("content", {})
                print(f"  Title: {content.get('title')}")
                print(f"  Description: {content.get('summary')}")
            print()
