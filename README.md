# ₿ Real-Time Bitcoin Streaming ETL Project ₿

## 📖 Overview

This project implements a scalable, real-time streaming ETL (Extract, Transform, Load) pipeline for Bitcoin cryptocurrency data on Google Cloud Platform (GCP). It ingests live BTC-USD price data via the `[yfinance](https://pypi.org/project/yfinance/)` WebSocket API, publishes validated messages to **Google Cloud Pub/Sub** through a threaded producer/consumer pipeline, processes and aggregates data using Apache Beam on Google Cloud Dataflow, stores the results in BigQuery, and visualizes key metrics on a [live Streamlit dashboard](https://btc-dashboard-app-862053225903.us-central1.run.app/).

> **Note:** `yfinance` is a third-party, unofficial Python library. It is **not** an official Yahoo Finance API or product, and its data access methods may change without notice.

## 🏗️ Architecture

Project Flowchart

The pipeline consists of the following stages:

1. **Ingestion**: `message_controller.py` orchestrates a producer/consumer flow — `YFinanceManager` streams live BTC-USD ticks over WebSocket, `ThreadManager` queues validated messages, and `PubSubPublisher` publishes JSON payloads to **Google Cloud Pub/Sub**.
2. **Stream Processing**: An **Apache Beam** pipeline running on **Google Cloud Dataflow** reads from the Pub/Sub subscription. It applies:
  - **Windowing**: Fixed 60-second windows.
    - **Aggregation**: Calculates Min, Max, and Average Price, and Total Volume per window.
3. **Storage**: Aggregated data is written to **Google BigQuery** partitioned tables.
4. **Visualization**: A **[Streamlit** dashboard](https://btc-dashboard-app-862053225903.us-central1.run.app/) queries BigQuery to display real-time price charts and KPI cards.
5. **Infrastructure**: Managed via **Terraform**.

## 🛠️ Tech Stack

- **Language**: Python 🐍
- **Market Data**: `yfinance` (unofficial Yahoo Finance data access) 📈
- **Cloud Provider**: Google Cloud Platform (GCP) ☁️
- **Infrastructure as Code**: Terraform 🏗️
- **Containerization**: Docker 🐳
- **Compute**: Google Compute Engine (GCE), Cloud Run ⚡
- **Data Services**: Pub/Sub, Dataflow, BigQuery, Secret Manager 📡

## 📂 Project Structure

- `src/btc_streaming_etl/pubsub/message_controller.py`: Entry point that wires ingestion and publishing together.
- `src/btc_streaming_etl/pubsub/yfinance_manager.py`: WebSocket client for live BTC-USD price streaming via `yfinance`.
- `src/btc_streaming_etl/pubsub/thread_manager.py`: Producer/consumer threading layer with a bounded message queue.
- `src/btc_streaming_etl/pubsub/pubsub_publisher.py`: GCP Pub/Sub publisher client.
- `src/btc_streaming_etl/pubsub/data_validator.py`: Schema validation for incoming price messages.
- `src/btc_streaming_etl/dataflow/dataflow.py`: Apache Beam pipeline for streaming analytics and BigQuery insertion.
- `src/tests/`: Unit tests for yfinance, publisher, and threading modules.
- `btc_dashboard/main.py`: Streamlit application for data visualization.
- `terraform_gcp_resources/main.tf`: Terraform configuration defining GCP resources (APIs, Service Accounts, IAM, Artifact Registry).

> **Legacy:** `src/btc_streaming_etl/pubsub/pub_sub.py` is the original CoinGecko-based publisher and is retained for reference during the migration.

## ✨ Key Features

- **Secure Credential Management**: Uses GCP Secret Manager for accessing API keys and Service Account credentials.
- **Robust Error Handling**: Ingestion validates message schemas, handles WebSocket disconnects, and surfaces GCP publish errors via `GoogleAPICallError`.
- **Scalability**: Leverages serverless technologies (Pub/Sub, Dataflow, Cloud Run) to handle varying loads.
- **IaC**: Fully reproducible infrastructure state using Terraform.

## 🚀 Future Improvements

- Implement Cloud Monitoring alerts for pipeline lag or ingestion failures.
- Add Simple Moving Average (SMA) calculations to the Dataflow pipeline.
- Optimize BigQuery costs with clustering on the `event_timestamp`.
- Implement web sockets to reduce latency of chart updates. 
- Implement machine learning models to utilize time series analysis to predict future price trends of Bitcoin.

## 📜 License

This project is for educational purposes and portfolio demonstration.