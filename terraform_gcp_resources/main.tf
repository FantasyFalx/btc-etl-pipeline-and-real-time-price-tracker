## Variable Defintions: ##

variable "service_account_display_names" {
  type        = list(string)
  description = "List of service account display names"
}

variable "api_services" {
  type        = list(string)
  description = "List of enabled GCP APIs"
}

variable "service_account_ids" {
  type        = list(string)
  description = "List of service account IDs"
}

variable "repository_ids" {
  type        = list(string)
  description = "List of repository IDs"
}

variable "service_account_roles" {
  type        = list(string)
  description = "List of IAM roles bound to service accounts; index usage defined in main.tf"
}

variable "storage_bucket_names" {
  type        = list(string)
  description = "List of GCS bucket names"
}

variable "storage_bucket_iam_roles" {
  type        = list(string)
  description = "IAM roles for GCS bucket bindings; index usage defined in main.tf"
}

variable "pubsub_topic_ids" {
  type        = list(string)
  description = "List of Pub/Sub topic IDs"
}

variable "pubsub_subscription_ids" {
  type        = list(string)
  description = "List of Pub/Sub subscription IDs"
}

variable "pubsub_topic_iam_roles" {
  type        = list(string)
  description = "IAM roles for Pub/Sub topic bindings; index usage defined in main.tf"
}

variable "pubsub_subscription_iam_roles" {
  type        = list(string)
  description = "IAM roles for Pub/Sub subscription bindings; index usage defined in main.tf"
}

variable "artifact_registry_iam_roles" {
  type        = list(string)
  description = "IAM roles for Artifact Registry repo bindings; index usage defined in main.tf"
}

variable "service_account_user_roles" {
  type        = list(string)
  description = "IAM roles for service account impersonation bindings; index usage defined in main.tf"
}

variable "bigquery_dataset_ids" {
  type        = list(string)
  description = "List of BigQuery dataset IDs"
}

variable "bigquery_dataset_locations" {
  type        = list(string)
  description = "List of BigQuery dataset locations; index matches bigquery_dataset_ids"
}

variable "bigquery_table_ids" {
  type        = list(string)
  description = "List of BigQuery table IDs"
}

variable "bigquery_dataset_iam_roles" {
  type        = list(string)
  description = "IAM roles for BigQuery dataset bindings; index usage defined in main.tf"
}

variable "project_id" {
  type        = string
  description = "The GCP project ID where resources will be created"

  validation {
    condition     = length(var.project_id) > 0
    error_message = "project_id must not be empty"
  }
}

variable "region" {
  type        = string
  description = "The GCP region for regional resources"
  default     = "us-central1"
}


########################################################

## Terraform Provider Configuration ##

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.8.0"
    }
  }
}


provider "google" {
  project = var.project_id
}

data "google_project" "project" {
  project_id = var.project_id
}

locals {
  default_compute_service_account = "${data.google_project.project.number}-compute@developer.gserviceaccount.com"
}


########################################################

## Enabled GCP APIs ##

resource "google_project_service" "project" {
  project = var.project_id
  service = var.api_services[0]
}

resource "google_project_service" "compute" {
  project = var.project_id
  service = var.api_services[3]
}

resource "google_project_service" "storage" {
  project = var.project_id
  service = var.api_services[4]
}

resource "google_project_service" "dataflow" {
  project = var.project_id
  service = var.api_services[1]
}

resource "google_project_service" "bigquery" {
  project = var.project_id
  service = var.api_services[2]
}

resource "google_project_service" "artifact_registry" {
  project = var.project_id
  service = var.api_services[5]
}

resource "google_project_service" "cloud_run" {
  project = var.project_id
  service = var.api_services[6]
}

########################################################

## Service Accounts ##

resource "google_service_account" "pub_sub_deployer_service_account" {
  account_id   = var.service_account_ids[3]
  display_name = var.service_account_display_names[3]
}

resource "google_service_account" "dataflow_service_account" {
  account_id   = var.service_account_ids[0]
  display_name = var.service_account_display_names[0]
}

resource "google_service_account" "compute_service_account" {
  account_id   = var.service_account_ids[1]
  display_name = var.service_account_display_names[1]
}

resource "google_service_account" "storage_service_account" {
  account_id   = var.service_account_ids[2]
  display_name = var.service_account_display_names[2]
}

########################################################

## Dataflow Service Account (project-level) ##

resource "google_project_iam_member" "dataflow_worker_binding" {
  project = var.project_id
  role    = var.service_account_roles[13]
  member  = "serviceAccount:${google_service_account.dataflow_service_account.email}"
}

resource "google_project_iam_member" "dataflow_storage_binding" {
  project = var.project_id
  role    = var.service_account_roles[1]
  member  = "serviceAccount:${google_service_account.dataflow_service_account.email}"
}

resource "google_project_iam_member" "dataflow_pubsub_viewer_binding" {
  project = var.project_id
  role    = var.service_account_roles[11]
  member  = "serviceAccount:${google_service_account.dataflow_service_account.email}"
}

resource "google_project_iam_member" "dataflow_cloudbuild_editor_binding" {
  project = var.project_id
  role    = var.service_account_roles[12]
  member  = "serviceAccount:${google_service_account.dataflow_service_account.email}"
}

resource "google_project_iam_member" "dataflow_artifact_registry_writer_binding" {
  project = var.project_id
  role    = var.service_account_roles[9]
  member  = "serviceAccount:${google_service_account.dataflow_service_account.email}"
}

########################################################

## Pub/Sub Deployer Service Account (CI/CD) ##

resource "google_project_iam_member" "deployer_run_admin_binding" {
  project = var.project_id
  role    = var.service_account_roles[8]
  member  = "serviceAccount:${google_service_account.pub_sub_deployer_service_account.email}"
}

resource "google_project_iam_member" "deployer_artifact_registry_writer_binding" {
  project = var.project_id
  role    = var.service_account_roles[9]
  member  = "serviceAccount:${google_service_account.pub_sub_deployer_service_account.email}"
}

resource "google_project_iam_member" "deployer_artifact_registry_reader_binding" {
  project = var.project_id
  role    = var.service_account_roles[10]
  member  = "serviceAccount:${google_service_account.pub_sub_deployer_service_account.email}"
}

resource "google_project_iam_member" "deployer_dataflow_admin_binding" {
  project = var.project_id
  role    = var.service_account_roles[0]
  member  = "serviceAccount:${google_service_account.pub_sub_deployer_service_account.email}"
}

resource "google_storage_bucket_iam_member" "deployer_staging_object_creator_binding" {
  bucket = google_storage_bucket.dataflow_staging.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.pub_sub_deployer_service_account.email}"
}

########################################################

## Artifact Registry ##

resource "google_artifact_registry_repository" "pubsub_script_repo" {
  location      = var.region
  repository_id = var.repository_ids[0]
  description   = "Repo to store container for published scripts"
  format        = "DOCKER"

  depends_on = [google_project_service.artifact_registry]
}

resource "google_artifact_registry_repository_iam_member" "deployer_writer_repo_binding" {
  project    = var.project_id
  location   = var.region
  repository = google_artifact_registry_repository.pubsub_script_repo.name
  role       = var.artifact_registry_iam_roles[0]
  member     = "serviceAccount:${google_service_account.pub_sub_deployer_service_account.email}"
}

resource "google_artifact_registry_repository_iam_member" "dataflow_writer_repo_binding" {
  project    = var.project_id
  location   = var.region
  repository = google_artifact_registry_repository.pubsub_script_repo.name
  role       = var.artifact_registry_iam_roles[0]
  member     = "serviceAccount:${google_service_account.dataflow_service_account.email}"
}

resource "google_artifact_registry_repository_iam_member" "compute_reader_repo_binding" {
  project    = var.project_id
  location   = var.region
  repository = google_artifact_registry_repository.pubsub_script_repo.name
  role       = var.artifact_registry_iam_roles[1]
  member     = "serviceAccount:${google_service_account.compute_service_account.email}"
}

resource "google_artifact_registry_repository_iam_member" "default_compute_reader_repo_binding" {
  project    = var.project_id
  location   = var.region
  repository = google_artifact_registry_repository.pubsub_script_repo.name
  role       = var.artifact_registry_iam_roles[1]
  member     = "serviceAccount:${local.default_compute_service_account}"
}

resource "google_storage_bucket_iam_member" "default_compute_staging_binding" {
  bucket = google_storage_bucket.dataflow_staging.name
  role   = var.storage_bucket_iam_roles[0]
  member = "serviceAccount:${local.default_compute_service_account}"
}

resource "google_service_account_iam_member" "compute_sa_cd_actas_binding" {
  service_account_id = google_service_account.compute_service_account.name
  role               = var.service_account_user_roles[0]
  member             = "serviceAccount:${google_service_account.pub_sub_deployer_service_account.email}"
}

resource "google_service_account_iam_member" "dataflow_sa_cd_actas_binding" {
  service_account_id = google_service_account.dataflow_service_account.name
  role               = var.service_account_user_roles[0]
  member             = "serviceAccount:${google_service_account.pub_sub_deployer_service_account.email}"
}

########################################################

## Compute Service Account (Cloud Run runtime) ##

resource "google_project_iam_member" "compute_run_admin_binding" {
  project = var.project_id
  role    = var.service_account_roles[5]
  member  = "serviceAccount:${google_service_account.compute_service_account.email}"
}

resource "google_project_iam_member" "compute_artifact_registry_reader_binding" {
  project = var.project_id
  role    = var.service_account_roles[7]
  member  = "serviceAccount:${google_service_account.compute_service_account.email}"
}

########################################################

## Storage Service Account (project-level) ##

resource "google_project_iam_member" "storage_admin_binding" {
  project = var.project_id
  role    = var.service_account_roles[4]
  member  = "serviceAccount:${google_service_account.storage_service_account.email}"
}

########################################################

## Pipeline Resources ##

locals {
  bitcoin_streaming_table_schema = jsonencode([
    { name = "id", type = "STRING", mode = "NULLABLE" },
    { name = "price", type = "FLOAT", mode = "NULLABLE" },
    { name = "time", type = "STRING", mode = "NULLABLE" },
    { name = "currency", type = "STRING", mode = "NULLABLE" },
    { name = "exchange", type = "STRING", mode = "NULLABLE" },
    { name = "quote_type", type = "INTEGER", mode = "NULLABLE" },
    { name = "market_hours", type = "INTEGER", mode = "NULLABLE" },
    { name = "change_percent", type = "FLOAT", mode = "NULLABLE" },
    { name = "day_volume", type = "STRING", mode = "NULLABLE" },
    { name = "day_high", type = "FLOAT", mode = "NULLABLE" },
    { name = "day_low", type = "FLOAT", mode = "NULLABLE" },
    { name = "change", type = "FLOAT", mode = "NULLABLE" },
    { name = "open_price", type = "FLOAT", mode = "NULLABLE" },
    { name = "last_size", type = "STRING", mode = "NULLABLE" },
    { name = "price_hint", type = "STRING", mode = "NULLABLE" },
    { name = "vol_24hr", type = "STRING", mode = "NULLABLE" },
    { name = "vol_all_currencies", type = "STRING", mode = "NULLABLE" },
    { name = "from_currency", type = "STRING", mode = "NULLABLE" },
    { name = "circulating_supply", type = "FLOAT", mode = "NULLABLE" },
    { name = "market_cap", type = "FLOAT", mode = "NULLABLE" },
  ])
}

## GCS (Dataflow staging) ##

resource "google_storage_bucket" "dataflow_staging" {
  name                        = var.storage_bucket_names[0]
  location                    = var.region
  project                     = var.project_id
  uniform_bucket_level_access = true
  force_destroy               = false

  depends_on = [google_project_service.storage]
}

## Pub/Sub ##

resource "google_pubsub_topic" "btc_price" {
  name    = var.pubsub_topic_ids[0]
  project = var.project_id

  depends_on = [google_project_service.project]
}

resource "google_pubsub_topic_iam_member" "compute_publisher_binding" {
  topic  = google_pubsub_topic.btc_price.name
  role   = var.pubsub_topic_iam_roles[0]
  member = "serviceAccount:${google_service_account.compute_service_account.email}"
}

resource "google_project_iam_member" "compute_pubsub_publisher_binding" {
  project = var.project_id
  role    = var.service_account_roles[6]
  member  = "serviceAccount:${google_service_account.compute_service_account.email}"
}

resource "google_pubsub_subscription" "btc_pull" {
  name    = var.pubsub_subscription_ids[0]
  topic   = google_pubsub_topic.btc_price.name
  project = var.project_id

  ack_deadline_seconds = 20

  depends_on = [google_project_service.project]
}

resource "google_pubsub_subscription_iam_member" "dataflow_subscriber_binding" {
  subscription = google_pubsub_subscription.btc_pull.name
  role         = var.pubsub_subscription_iam_roles[0]
  member       = "serviceAccount:${google_service_account.dataflow_service_account.email}"
}

resource "google_project_iam_member" "dataflow_pubsub_subscriber_binding" {
  project = var.project_id
  role    = var.service_account_roles[3]
  member  = "serviceAccount:${google_service_account.dataflow_service_account.email}"
}

## BigQuery ##

resource "google_bigquery_dataset" "streaming" {
  dataset_id = var.bigquery_dataset_ids[0]
  location   = var.bigquery_dataset_locations[0]
  project    = var.project_id

  depends_on = [google_project_service.bigquery]
}

resource "google_bigquery_dataset_iam_member" "dataflow_editor_binding" {
  dataset_id = google_bigquery_dataset.streaming.dataset_id
  role       = var.bigquery_dataset_iam_roles[0]
  member     = "serviceAccount:${google_service_account.dataflow_service_account.email}"
}

resource "google_project_iam_member" "dataflow_bigquery_binding" {
  project = var.project_id
  role    = var.service_account_roles[2]
  member  = "serviceAccount:${google_service_account.dataflow_service_account.email}"
}

resource "google_bigquery_table" "streaming" {
  dataset_id = google_bigquery_dataset.streaming.dataset_id
  table_id   = var.bigquery_table_ids[0]
  project    = var.project_id
  schema     = local.bitcoin_streaming_table_schema

  deletion_protection = false
}

########################################################