terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
  required_version = ">= 0.13"
}

provider "yandex" {
  cloud_id                 = var.cloud_id
  folder_id                = var.folder_id
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
    "yandex_access_key" = var.yandex_access_key,
    "yandex_secret_key" = var.yandex_secret_key,
    "cloud_id"          = var.cloud_id,
    "folder_id"         = var.folder_id,
    "tg_bot_key"        = var.tg_bot_key
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

resource "yandex_function_iam_binding" "function-aim-f" {
  function_id = yandex_function.function.id
  role        = "serverless.functions.invoker"

  members = [
    "system:allUsers"
  ]
}

variable "cloud_id" {
  type        = string
  description = "Идентификатор облака"
}

variable "folder_id" {
  type        = string
  description = "Идентификатор папки"
}

variable "yandex_access_key" {
  type        = string
  description = "Идентификатор статичного ключа"
}

variable "yandex_secret_key" {
  type        = string
  description = "Секретный ключ"
}

variable "tg_bot_key" {
  type        = string
  description = "Бот ключ"
}

data "http" "register_bot_url" {
  url = "https://api.telegram.org/bot${var.tg_bot_key}/setWebhook?url=https://functions.yandexcloud.net/${yandex_function.function.id}"
}