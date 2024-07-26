variable "prefix" {
    description = "The prefixed used for all resources in this environment"
}

variable "app_service_name" {
    description = "App Service Name"
    default = "cb-todo-app-tf"
    sensitive = false
}

variable "login_disabled" {
  description = "Used to disable/enable github oauth login"
  default = "False"
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

variable "key_vault_rand_str" {
  description = "random string for test key vault"
  default = ""
}

variable "db_account_name" {
  description = "Name of db storage account"
}

variable "mongo_connection_string" {
  description = "mongo DB connection string"  
}

variable "log_level" {
  description = "level of logging"
  default = "ERROR"
}

variable "loggly_token" {
  sensitive = true
  default = ""
}