## Variable Defintions: ##

# Basic Configs
variable "project_id" {
  type = string
  description = "The GCP project ID where resources will be created"
  
  validation {
    condition     = length(var.project_id) > 0
    error_message = "project_id must not be empty"
  }
}

variable "region" {
  type = string
  description = "The GCP region for regional resources"
  default     = "us-central1"
}

# Pub/Sub 
variable pubsub_sa_id {
  type = string
  description = "Pub/Sub Service Account ID"
}


variable pubsub_sa_display_name {
  type = string
  description = "Pub/Sub Service Account Display Name"
}


# Dataflow 
variable dataflow_sa_id {
  type = string
  description = "Dataflow Service Account ID"
}

variable dataflow_sa_display_name {
  type = string
  description = "Dataflow Service Account Display Name"
}

# Big Query

variable bigquery_sa_id {
  type = string
  description = "Big Query Service Account ID"
}

variable bigquery_sa_display_name {
  type = string
  description = "Big Query Service Account Display Name"
}

# Cloud Storage 
variable gcs_sa_id {
  type = string
  description = "Cloud Storage Service Account ID"
}

variable gcs_sa_display_name {
  type = string
  description = "Service account display name"
  default = "value"
}


# Secret manager
variable secret_manager_sa_id {
  type = string
  description = "Service account secret id"
}

variable secret_manager_sa_display_name {
  type = string
  description = "Service account display name"
}

# Artifact registry
variable "pub_sub_repo_id" {
  type = string
  description = "Pub/Sub artifact registry repository id"
}

variable "dashboard_repo_id" {
  type = string
  description = "Dashboard artifact registry repository id"
}

############################################################

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
  project = var.project_id
}

### Resources ###############################

#---- API Resources --------------------------

## Pub/Sub API
resource "google_project_service" "project" {
  project = var.project_id
  service = "pubsub.googleapis.com"
}

## Dataflow API
resource "google_project_service" "dataflow" {
  project = var.project_id
  service = "dataflow.googleapis.com"
}

## BigQuery API
resource "google_project_service" "bigquery" {
  project = var.project_id
  service = "bigquery.googleapis.com"
}

## GCS API

resource "google_project_service" "cloud_storage" {
  project = var.project_id
  service = "storage.googleapis.com"
}

## Cloud Monitoring API
resource "google_project_service" "cloud_monitoring" {
  project = var.project_id
  service = "monitoring.googleapis.com"
}


## Cloud Scheduler API
resource "google_project_service" "scheduler" {
  project = var.project_id
  service = "cloudscheduler.googleapis.com"
}

## Cloud Run API
resource "google_project_service" "cloud_run" {
  project = var.project_id
  service = "run.googleapis.com"
}

## Compute Engine API
resource "google_project_service" "compute_api" {
  project = var.project_id
  service = "compute.googleapis.com"
}

#-- Service Account Resources ------------------

# PUB/SUB Service Account
resource "google_service_account" "pubsub_service_account" {
  account_id   = var.pubsub_sa_id
  display_name = var.pubsub_sa_display_name
}

resource "google_project_iam_member" "pub_sub_admin_binding" {
  # A hopefully this reference works
  project = var.project_id
  role    = "roles/pubsub.admin"
  # .'s are for the attribute variables
  member = "serviceAccount:${google_service_account.pubsub_service_account.email}"
}

# Dataflow Service Account
resource "google_service_account" "data_flow_service_account" {
  account_id   = var.dataflow_sa_id
  display_name = var.dataflow_sa_display_name
}

resource "google_project_iam_member" "data_flow_admin_binding" {
  # A hopefully this reference works
  project = var.project_id
  role    = "roles/dataflow.admin"
  # .'s are for the attribute variables
  member = "serviceAccount:${google_service_account.data_flow_service_account.email}"
}

# BigQuery Service Account
resource "google_service_account" "bigquery_service_account" {
  account_id   = var.bigquery_sa_id
  display_name = var.bigquery_sa_display_name
}

resource "google_project_iam_member" "bigquery_admin_binding" {
  # A hopefully this reference works
  project = var.project_id
  role    = "roles/bigquery.admin"
  # .'s are for the attribute variables
  member = "serviceAccount:${google_service_account.bigquery_service_account.email}"
}

# GCS Service Account
resource "google_service_account" "gcs_service_account" {
  account_id   = var.gcs_sa_id
  display_name = var.gcs_sa_display_name
}

resource "google_project_iam_member" "gcs_admin_binding" {
  # A hopefully this reference works
  project = var.project_id
  role    = "roles/storage.objectAdmin"
  # .'s are for the attribute variables
  member = "serviceAccount:${google_service_account.gcs_service_account.email}"
}

# Secret Manager Service Account
resource "google_service_account" "secret_manager_service_account" {
  account_id   = var.secret_manager_sa_id
  display_name = var.secret_manager_sa_display_name
}

resource "google_project_iam_member" "secret_manager" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.secret_manager_service_account.email}"
}

### Artifact Registry Creation ########################

# Pub/sub Container
resource "google_artifact_registry_repository" "pub_sub_script_repo" {
  location      = var.region
  repository_id = var.pub_sub_repo_id
  description   = "Repo to store container for pub-sub script"
  format        = "DOCKER"
}

# Streamlit dashboard container
resource "google_artifact_registry_repository" "dashboard_application_repo" {
  location      = var.region
  repository_id = var.dashboard_repo_id
  description   = "Repo to store streamlit dashboard application."
  format        = "DOCKER"
}


###############################################
 