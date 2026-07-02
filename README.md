# ₿ Real-Time Bitcoin Streaming ETL Project ₿

### Version: 2.0.0

## 📖 Project Overview

This project implements a scalable, real-time streaming ETL (Extract, Transform, Load) pipeline for Bitcoin cryptocurrency data on Google Cloud Platform (GCP). It ingests live BTC-USD price data via the [yfinance](https://pypi.org/project/yfinance/) WebSocket API, publishes validated messages to **Google Cloud Pub/Sub** through a threaded producer/consumer pipeline, processes and aggregates data using **Apache Beam** on **Google Cloud Dataflow**, and stores the results in **BigQuery**.

> **Note:** `yfinance` is a third-party, unofficial Python library. It is **not** an official Yahoo Finance API or product, and its data access methods may change without notice.



## 🏗️ Architecture

The pipeline consists of the following stages:

1. **Ingestion**
  - `message_controller.py` orchestrates a **multi-threaded producer/consumer flow**:
  - `YFinanceManager` streams live BTC-USD ticks over WebSocket.
  - `ThreadManager` queues validated messages.
  - `PubSubPublisher` publishes JSON payloads to **Google Cloud Pub/Sub**.
2. **Stream Processing**
  - An **Apache Beam** pipeline running on **Google Cloud Dataflow** reads from the Pub/Sub subscription and applies transforms.
3. **Storage**
  - Aggregated data is written to **Google BigQuery**.
4. **Infrastructure**
  - Managed via **Terraform**.



## 🛠️ Tech Stack

- **Language**: Python 🐍
- **Market Data**: `yfinance` (unofficial Yahoo Finance data access) 📈
- **Cloud Provider**: Google Cloud Platform (GCP) ☁️
- **Infrastructure as Code**: Terraform 🏗️
- **Containerization**: Docker 🐳
- **Compute**: Google Compute Engine (GCE), Cloud Run ⚡
- **Data Services**: Pub/Sub, Dataflow, BigQuery



## 📂 Project Structure

- `src/btc_streaming_etl/pubsub/message_controller.py`  
Entry point that wires ingestion and publishing together.
- `src/btc_streaming_etl/pubsub/yfinance_manager.py`  
WebSocket client for live BTC-USD price streaming via `yfinance`.
- `src/btc_streaming_etl/pubsub/thread_manager.py`  
Producer/consumer threading layer with a bounded message queue.
- `src/btc_streaming_etl/pubsub/pubsub_publisher.py`  
GCP Pub/Sub publisher client.
- `src/btc_streaming_etl/pubsub/data_validator.py`  
Schema validation for incoming price messages.
- `src/btc_streaming_etl/dataflow/pipeline.py`  
Apache Beam pipeline for streaming analytics and BigQuery insertion.
- `src/tests/`  
Unit tests for yfinance, publisher, and threading modules.
- `terraform_gcp_resources/main.tf`  
Terraform configuration defining GCP resources (APIs, Service Accounts, IAM, Artifact Registry).



## ✨ Key Features

- **Robust Error Handling:** Ingestion validates message schemas, handles WebSocket disconnects, and surfaces GCP publish errors via `GoogleAPICallError`.
- **Testing:** Unit tests cover yfinance integration, message schema validation, Pub/Sub publishing, and multithreaded processing.
- **Scalability:** Leverages serverless technologies (Pub/Sub, Dataflow, Cloud Run) to handle varying loads.
- **IaC:** Fully reproducible infrastructure state using Terraform.



## 📝 Steps to Duplicate and Run Pipeline

1. Clone the git repo to your local machine:
  ```bash
    git clone https://github.com/FantasyFalx/btc-etl-pipeline-and-real-time-price-tracker
  ```
2. Create a new branch:
  ```bash
    git checkout -b <my_branch_name>
  ```
3. Create the variable file Terraform needs to build the cloud resources:
  ```bash
    cp terraform_gcp_resources/terraform.tfvars.example terraform_gcp_resources/production.auto.tfvars
  ```
4. Edit `production.auto.tfvars` with the required values.
5. Initialize and create the GCP resources:
  ```bash
    cd terraform_gcp_resources
    terraform init
    terraform fmt
    terraform validate
    terraform apply
  ```
6. In the GCP console:
  - Go to **IAM** > **Service Accounts**.
    - Open `pub-sub-deployer-8888@<your-project-id>.iam.gserviceaccount.com` (deployer account from Terraform).
    - Create and download a JSON key for this service account. **Do not commit this key to the repository.**
7. In your GitHub repository:
  - Go to **Settings** > **Secrets and variables** > **Actions** > **New repository secret**
    - Paste the full contents of the downloaded JSON key file.
    - Set the secret name to `BUILD_AND_DEPLOY_KEY`.
8. Still in GCP **Service Accounts**, copy the runtime account emails (replace `<your-project-id>` with your GCP project ID):
  - `compute-8888@<your-project-id>.iam.gserviceaccount.com`
  - `data-flow-9999@<your-project-id>.iam.gserviceaccount.com`
9. In GitHub:
  - Add these service account emails as new repository secrets.
    - Set the names to `COMPUTE_SERVICE_ACCOUNT_EMAIL` and `DATAFLOW_SERVICE_ACCOUNT_EMAIL`.
10. Back in your repository terminal, commit and push any intended changes (`production.auto.tfvars` is gitignored and must not be committed):
  ```bash
    git add .
    git commit -m "<my_commit_message>"
  ```
11. Push your branch:
  ```bash
    git push origin <my_branch_name>
  ```
12. Create a pull request, wait for the `ci.yml` script to execute, and after it passes, merge into `main`.
13. In GitHub **Actions**, monitor the `cd.yml` workflow to ensure build, push, and deploy steps succeed for both images.
14. In GCP console, verify your Cloud Run jobs, Dataflow pipelines, and BigQuery datasets/tables are present and active.
15. In BigQuery, preview your table to verify that BTC price data is streaming.



## 🚀 Future Improvements

- Implement Cloud Monitoring alerts for pipeline lag or ingestion failures.
- Add Simple Moving Average (SMA) calculations to the Dataflow pipeline.
- Implement machine learning models to utilize time series analysis to predict future price trends of Bitcoin.



## 📜 License

This project is for educational purposes and portfolio demonstration.