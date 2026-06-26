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


########################################################

## Cloud Resources ##

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


resource "google_project_iam_member" "data_flow_admin_binding" {
  project = var.project_id
  role    = "roles/dataflow.admin"
  member  = "serviceAccount:${google_service_account.dataflow_service_account.email}"
}


resource "google_artifact_registry_repository" "pubsub_script_repo" {
  location      = var.region
  repository_id = var.repository_ids[0]
  description   = "Repo to store container for published scripts"
  format        = "DOCKER"
}

########################################################