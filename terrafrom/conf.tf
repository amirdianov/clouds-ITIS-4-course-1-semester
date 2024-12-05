terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
  required_version = ">= 0.13"
}

provider "yandex" {
  cloud_id                 = var.CLOUD_ID
  folder_id                = var.FOLDER_ID
  service_account_key_file = "/home/ubuntu/tf-key/key.json"
}

resource "yandex_storage_bucket" "bucket" {
  bucket = "vvot-25-hw1-bucket"
}

resource "yandex_storage_object" "text_config" {
  bucket = yandex_storage_bucket.bucket.id
  source = "/home/ubuntu/hw/hw_1/text_config.txt"
  key    = "instruction.txt"
}

variable "CLOUD_ID" {
  type        = string
  description = "Идентификатор облака"
}

variable "FOLDER_ID" {
  type        = string
  description = "Идентификатор папки"
}
