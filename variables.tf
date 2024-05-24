variable "prefix" {
    description = "The prefixed used for all resources in this environment"
}

variable "app_service_name" {
    description = "App Service Name"
    default = "cb-todo-app-tf"
    sensitive = false
}

variable "secret_key" {
    description = "Flask session secret key"
    sensitive = true
}

variable "github_oauth_client_id" {
  sensitive = true
}

variable "github_oauth_client_secret" {
  sensitive = true
}

variable "mongo_database_name" {
  sensitive = true
}