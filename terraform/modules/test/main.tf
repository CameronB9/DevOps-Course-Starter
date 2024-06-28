provider "azurerm" {
	features {
		key_vault {
			purge_soft_delete_on_destroy = false
			recover_soft_deleted_key_vaults = true
		}
	}
}

resource "random_string" "azurerm_key_vault_name" {
  length  = 8
  lower   = true
  numeric = false
  special = false
  upper   = false
}

terraform {
	required_providers {
		azurerm = {
			source = "hashicorp/azurerm"
			version = ">= 3.8"
		}
	}

	backend "azurerm" {
		resource_group_name = "Cohort28_CamBod_ProjectExercise"
		storage_account_name = "cbtodoapptfstate"
		container_name = "cbtodoapptfstatectr"
		key = "test.terraform.tfstate"
	}
}

data "azurerm_resource_group" "main" {
    name = "Cohort28_CamBod_ProjectExercise"
}

resource "azurerm_cosmosdb_account" "unprotected" {
	name                = "${var.prefix}-cb-todo-app-db-acc-tf"
	location            = data.azurerm_resource_group.main.location
	resource_group_name = data.azurerm_resource_group.main.name
	offer_type          = "Standard"
	kind                = "MongoDB"

	capabilities {
		name = "EnableAggregationPipeline"
	}

	capabilities {
		name = "mongoEnableDocLevelTTL"
	}

	capabilities {
		name = "MongoDBv3.4"
	}

	capabilities {
		name = "EnableMongo"
	}

	capabilities {
		name = "EnableServerless"
	}

	consistency_policy {
		consistency_level       = "BoundedStaleness"
		max_interval_in_seconds = 300
		max_staleness_prefix    = 100000
	}

	geo_location {
		location          = data.azurerm_resource_group.main.location
		failover_priority = 0
	}

	lifecycle {
		prevent_destroy = false
	}

}

module "base" {
  source = "../base"
  prefix = "test"
  login_disabled = "True"
  mongo_database_name = var.mongo_database_name
  secret_key = var.secret_key
  github_oauth_client_id = var.github_oauth_client_id
  github_oauth_client_secret = var.github_oauth_client_secret
  key_vault_rand_str = "-${random_string.azurerm_key_vault_name.result}"
  db_account_name = azurerm_cosmosdb_account.unprotected.name
  mongo_connection_string = azurerm_cosmosdb_account.unprotected.primary_mongodb_connection_string
  log_level = var.log_level
}