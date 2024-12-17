terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
    telegram = {
      source = "yi-jiayu/telegram"
    }
  }
  required_version = ">= 0.13"
}

provider "telegram" {
  bot_token = var.tg_bot_key
}

resource "telegram_bot_webhook" "my_bot" {
  url = "https://api.telegram.org/bot${var.tg_bot_key}/setWebhook?url=https://functions.yandexcloud.net/${yandex_function.function.id}"
}


provider "yandex" {
  cloud_id                 = var.cloud_id
  folder_id                = var.folder_id
  service_account_key_file = pathexpand("~/tf-key/key.json")
}

resource "yandex_storage_bucket" "bucket" {
  bucket = var.bucket_name
}

resource "yandex_storage_object" "text_config" {
  bucket = yandex_storage_bucket.bucket.id
  source = pathexpand("~/src_new/instruction.txt")
  key    = var.bucket_key
}

resource "yandex_iam_service_account" "sa" {
  name        = "sa-hw1"
  description = "service account"
}

resource "yandex_resourcemanager_folder_iam_member" "sa-admin" {
  folder_id = var.folder_id
  role      = "admin"
  member    = "serviceAccount:${yandex_iam_service_account.sa.id}"
}

resource "yandex_iam_service_account_static_access_key" "sa-static-key" {
  service_account_id = yandex_iam_service_account.sa.id
  description        = "static access key"
}


resource "yandex_function" "function" {
  name       = "vvot-25-hw1-function"
  user_hash  = data.archive_file.zip.output_sha256
  runtime    = "python312"
  entrypoint = "bot.handler"
  service_account_id = "${yandex_iam_service_account.sa.id}"
  memory     = 128
  execution_timeout = 30
  environment = {
    "yandex_access_key" = yandex_iam_service_account_static_access_key.sa-static-key.access_key,
    "yandex_secret_key" = yandex_iam_service_account_static_access_key.sa-static-key.secret_key,
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

variable "tg_bot_key" {
  type        = string
  description = "Бот ключ"
}

variable "bucket_name" {
  type        = string
  description = "Название бакета"
}

variable "bucket_key" {
  type        = string
  description = "Ключ для объекта бакета"
}
