# Data Ingestion for Market Volatility

- Python for the extraction
- Bigquery tables in a dataset for accumulating the data
- Containerizing the python scripts
- Building and pushing the docker image to the artifact registry (gcr.io)
- Adding job to Cloud Run
- Creating Triggers to run it periodically

### Python for extraction

Folder structure

```
.
├── bq_data
│   ├── coindesk_bq.json
│   ├── cointelegraph_bq.json
│   ├── cryptopanic_bq.json
│   ├── newsdata_bq.json
│   ├── reddit_data_bq.json
│   ├── yfinance_news_bq.json
│   └── yfinance_tickers_bq.json
├── docker-compose.yml
├── Dockerfile
├── extracted_data
│   ├── coindesk.json
│   ├── cointelegraph.json
│   ├── cryptopanic.json
│   ├── newsdata.json
│   ├── reddit_data.json
│   ├── yfinance_news.json
│   └── yfinance_tickers.json
├── extractors
│   ├── coindesk.py
│   ├── cointelegraph.py
│   ├── cryptopanic.py
│   ├── newsdataio.py
│   ├── reddit.py
│   └── yfinance.py
├── gcloud
│   ├── bq.py
│   └── schemas.py
├── main.py
├── market-volatility-sa.json
├── pyproject.toml
├── README.md
├── sample.env
├── utils
│   └── file_utils.py
└── uv.lock
```

#### Data Sources

1. Coindesk news (RSS feed)
2. Cointelegraph news (RSS feed)
3. Coindesk (RSS feed)
4. NewsData.io News
5. Yfinance News
6. Yfinance Ticker data
7. Reddit – latest posts from relevant subreddits

- https://cryptopanic.com/developers/api/
- https://newsdata.io/search-news

- https://www.coindesk.com/markets
- https://www.coindesk.com/arc/outboundfeeds/rss

- https://cointelegraph.com/
- https://cointelegraph.com/rss

- Yfinance Ticker data
- Yfinance News for the cryptocurrency

- Reddit with few popular chosen subreddits
- `https://www.reddit.com/r/{subreddit}/new.json?limit={limit}`

---

### Packages Used

```
"fastfeedparser>=0.4.4",
"google-cloud-bigquery>=3.38.0",
"pandas>=2.3.3",
"python-dotenv>=1.2.1",
"requests>=2.32.5",
"yfinance>=0.2.66",
```

---

Transforming raw data to structured format and saving the extracted data in JSON format using `json` module before uploading to BigQuery.

---

Built an image from the repo using the following [Dockerfile](./Dcoekrfile)

```Dockerfile
version: "3.8"
services:
  data-ingestion-app:
    build: .
    environment:
      - GOOGLE_APPLICATION_CREDENTIALS=/app/market-volatility-sa.json
      - NEWSDATA_API_KEY=${NEWSDATA_API_KEY}
      - CRYPTOPANIC_API_KEY=${CRYPTOPANIC_API_KEY}
      - GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_APPLICATION_CREDENTIALS}
      - GCP_BQ_PROJECT_NAME=${GCP_BQ_PROJECT_NAME}
      - GCP_BQ_DATASET_NAME=${GCP_BQ_DATASET_NAME}
      - USE_CACHE=0
    volumes:
      - ./market-volatility-sa.json:/app/market-volatility-sa.json:ro # mount local key file read-only
```

---

### Login to gcloud cli

```
gcloud auth login
```

### Build latest with tag

Image Name is `ingestor`

```sh
docker build -t ingestor:latest .
```

```sh
$ docker image ls
$ docker tag <image-id-eg-3e4e8eb736e9> asia-south1-docker.pkg.dev/market-volatility/market-volatility-ingestion/ingestor
```

## Artifact Registry

### URL

```
asia-south1-docker.pkg.dev/market-volatility/market-volatility-ingestion/ingestor
```

### Describe the artifact registry

```
gcloud artifacts repositories describe market-volatility-ingestion \
    --project=market-volatility \
    --location=asia-south1
```

### Push container to artifact registry

```sh
$ docker push asia-south1-docker.pkg.dev/market-volatility/market-volatility-ingestion/ingestor
```

Select the image from the registry now in the cloud run job dashboard.

### Crontab for the scheduler

Every 12 hours
```
0 */12 * * *
```
