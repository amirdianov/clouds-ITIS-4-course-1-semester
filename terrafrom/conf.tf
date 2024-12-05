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

variable "CLOUD_ID" {
  type        = string
  description = "Идентификатор облака"
}

variable "FOLDER_ID" {
  type        = string
  description = "Идентификатор папки"
}
