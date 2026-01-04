# Cloud connection block
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.8.0"
    }
  }
}

# Provider
provider "google" {
  project = "bitcoin-streaming-etl-project"
}

### Resources ###############################

#---- API Resources --------------------------


## Pub/Sub API
resource "google_project_service" "project" {
  project = "bitcoin-streaming-etl-project"
  service = "pubsub.googleapis.com"
}

## Dataflow API

# Resource, than name of the terraform resource:
# resource <ACTUAL RESOURCE> <CUSTOM NAME FOR RESOURCE>

resource "google_project_service" "dataflow" {
  project = "bitcoin-streaming-etl-project"
  service = "dataflow.googleapis.com"
}

## BigQuery API

resource "google_project_service" "bigquery" {
  project = "bitcoin-streaming-etl-project"
  service = "bigquery.googleapis.com"
}

## GCS API

resource "google_project_service" "cloud_storage" {
  project = "bitcoin-streaming-etl-project"
  service = "storage.googleapis.com"
}

## Cloud Monitoring API

resource "google_project_service" "cloud_monitoring" {
  project = "bitcoin-streaming-etl-project"
  service = "monitoring.googleapis.com"
}


## Cloud Scheduler API

resource "google_project_service" "scheduler" {
  project = "bitcoin-streaming-etl-project"
  service = "cloudscheduler.googleapis.com"
}

## Cloud Run API
resource "google_project_service" "cloud_run" {
  project = "bitcoin-streaming-etl-project"
  service = "run.googleapis.com"
}

## Compute Engine API

resource "google_project_service" "compute_api" {
  project = "bitcoin-streaming-etl-project"
  service = "compute.googleapis.com"
}


#-- Service Account Resources ------------------

# Cloud Scheduler Service Account

resource "google_service_account" "cloud_scheduler_service_account" {
  account_id   = "cloud-scheduler-8888"
  display_name = "cloud-scheduler-controller"
}


# PUB/SUB Service Account (Role: Admin)
# Don't use underscores for resource creation
resource "google_service_account" "pubsub_service_account" {
  account_id   = "pub-sub-8888"
  display_name = "pub-sub-controller"
}

# IAM Member permission allows for the roles to be set.
resource "google_project_iam_member" "pub_sub_admin_binding" {
  # A hopefully this reference works
  project = "bitcoin-streaming-etl-project"
  role    = "roles/pubsub.admin"
  # .'s are for the attribute variables
  member = "serviceAccount:${google_service_account.pubsub_service_account.email}"
}

# Dataflow Service Account (Remove this)
resource "google_service_account" "data_flow_service_account" {
  account_id   = "data-flow-9999"
  display_name = "data-flow-controller"
}

# IAM Member permission allows for the roles to be set. (Remove this)
resource "google_project_iam_member" "data_flow_admin_binding" {
  # A hopefully this reference works
  project = "bitcoin-streaming-etl-project"
  role    = "roles/dataflow.admin"
  # .'s are for the attribute variables
  member = "serviceAccount:${google_service_account.data_flow_service_account.email}"
}

# BigQuery Service Account
resource "google_service_account" "bigquery_service_account" {
  account_id   = "big-query-8888"
  display_name = "big-query-controller"
}

# IAM Member permission allows for the roles to be set.
resource "google_project_iam_member" "bigquery_admin_binding" {
  # A hopefully this reference works
  project = "bitcoin-streaming-etl-project"
  role    = "roles/bigquery.admin"
  # .'s are for the attribute variables
  member = "serviceAccount:${google_service_account.bigquery_service_account.email}"
}

# Cloud Composer Service Account (REMOVE)
resource "google_service_account" "cloud_composer_service_account" {
  account_id   = "cloud-composer-8888"
  display_name = "cloud-composer-controller"
}

# IAM Member permission allows for the roles to be set. (REMOVE)
resource "google_project_iam_member" "cloud_composer_admin_binding" {
  # A hopefully this reference works
  project = "bitcoin-streaming-etl-project"
  role    = "roles/composer.admin"
  # .'s are for the attribute variables
  member = "serviceAccount:${google_service_account.cloud_composer_service_account.email}"
}

# GCS Service Account
resource "google_service_account" "gcs_service_account" {
  account_id   = "gcs-8888"
  display_name = "gcs-controller"
}

# IAM Member permission allows for the roles to be set.
resource "google_project_iam_member" "gcs_admin_binding" {
  # A hopefully this reference works
  project = "bitcoin-streaming-etl-project"
  role    = "roles/storage.objectAdmin"
  # .'s are for the attribute variables
  member = "serviceAccount:${google_service_account.gcs_service_account.email}"
}

# Cloud Monitoring Service Account
resource "google_service_account" "monitoring_service_account" {
  account_id   = "monitoring-account-8888"
  display_name = "mointoring-controller"
}

# IAM Member permission allows for the roles to be set.
resource "google_project_iam_member" "mointoring_viewer_binding" {
  # A hopefully this reference works
  project = "bitcoin-streaming-etl-project"
  role    = "roles/monitoring.viewer"
  # .'s are for the attribute variables
  member = "serviceAccount:${google_service_account.monitoring_service_account.email}"
}

# Secret Manager Service Account
resource "google_service_account" "secret_manager_service_account" {
  account_id   = "secret-manager-8888"
  display_name = "secret-manager-controller"
}

# IAM Member permission allows for the roles to be set.
resource "google_project_iam_member" "secret_manager" {
  project = "bitcoin-streaming-etl-project"
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.secret_manager_service_account.email}"
}

### Artifact Registry Creation ########################

# Pub/sub Container
resource "google_artifact_registry_repository" "pub_sub_script_repo" {
  location      = "us-central1"
  repository_id = "pub-sub-script-repo"
  description   = "Repo to store container for pub-sub script"
  format        = "DOCKER"
}

# Streamlit dashboard container
resource "google_artifact_registry_repository" "dashboard_application_repo" {
  location      = "us-central1"
  repository_id = "btc-dashboard-repo"
  description   = "Repo to store streamlit dashboard application."
  format        = "DOCKER"
}


# Container Deployments to cloud run for production use.
###############################################
 