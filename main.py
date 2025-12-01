from dotenv import load_dotenv

import gcloud.bq as bq
from extractors.coindesk import getCoinDesk
from extractors.cointelegraph import getCoinTelegraph
from extractors.cryptopanic import getCryptoPanicData
from extractors.newsdataio import getNewsData
from extractors.reddit import getRedditData
from extractors.yfinance import getYFinanceData

load_dotenv()


def main():
    print("Starting data extraction...\n")

    print("Fetching CoinTelegraph data:")
    ctdf = getCoinTelegraph()
    if ctdf is not None:
        bq.ingestCointelegraph(ctdf)

    print("\nFetching CoinDesk data:")
    cddf = getCoinDesk()
    if cddf is not None:
        bq.ingestCoindesk(cddf)

    print("\nFetching NewsData.io data:")
    nddf = getNewsData()
    if nddf is not None:
        bq.ingestNewsdata(nddf)

    print("\nFetching CryptoPanic data:")
    cpdf = getCryptoPanicData()
    if cpdf is not None:
        bq.ingestCryptopanic(cpdf)

    print("\nFetching YFinance data:")
    yfnewsdf, yftickerdf = getYFinanceData()
    if yfnewsdf is not None:
        bq.ingestYFinanceNews(yfnewsdf)
    if yftickerdf is not None:
        bq.ingestYFinanceTickers(yftickerdf)

    print("\nFetching Reddit data:")
    rdtdf = getRedditData()
    if rdtdf is not None:
        bq.ingestReddit(rdtdf)


if __name__ == "__main__":
    main()
