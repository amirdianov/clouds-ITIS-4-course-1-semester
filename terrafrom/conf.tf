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

resource "yandex_function" "function" {
  name       = "vvot-25-hw1-function"
  user_hash  = data.archive_file.zip.output_sha256
  runtime    = "python312"
  entrypoint = "bot.handler"
  service_account_id = "ajebfdo7fm8mv1mfl91q"
  memory     = 128
  execution_timeout = 30
  environment = {
    "YANDEX_ACCESS_KEY" = var.YANDEX_ACCESS_KEY,
    "YANDEX_SECRET_KEY" = var.YANDEX_SECRET_KEY,
    "CLOUD_ID"          = var.CLOUD_ID,
    "FOLDER_ID"         = var.FOLDER_ID,
    "TG_BOT_KEY"        = var.TG_BOT_KEY
  }
  content {
    zip_filename = data.archive_file.zip.output_path
  }
}

data "archive_file" "zip" {
  type        = "zip"
  output_path = "bot.zip"
  source_dir  = "src_new"
}

variable "CLOUD_ID" {
  type        = string
  description = "Идентификатор облака"
}

variable "FOLDER_ID" {
  type        = string
  description = "Идентификатор папки"
}

variable "YANDEX_ACCESS_KEY" {
  type        = string
  description = "Идентификатор статичного ключа"
}

variable "YANDEX_SECRET_KEY" {
  type        = string
  description = "Секретный ключ"
}

variable "TG_BOT_KEY" {
  type        = string
  description = "Бот ключ"
}
