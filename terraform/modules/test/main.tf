provider "azurerm" {
	features {
		key_vault {
			purge_soft_delete_on_destroy = false
			recover_soft_deleted_key_vaults = true
		}
	}
}

resource "random_string" "azurerm_key_vault_name" {
  length  = 5
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

module "base" {
  source = "../base"
  prefix = "test"
  login_disabled = "True"
  mongo_database_name = var.mongo_database_name
  secret_key = var.secret_key
  github_oauth_client_id = var.github_oauth_client_id
  github_oauth_client_secret = var.github_oauth_client_secret
  key_vault_rand_str = "-${random_string.azurerm_key_vault_name.result}"
  prevent_db_destroy = false
}