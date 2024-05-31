provider "azurerm" {
	features {
		key_vault {
			purge_soft_delete_on_destroy = false
			recover_soft_deleted_key_vaults = true
		}
	}
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
		key = "prod.terraform.tfstate"
	}
}

module "base" {
  source = "../base"
  prefix = "prod"
  mongo_database_name = var.mongo_database_name
  secret_key = var.secret_key
  github_oauth_client_id = var.github_oauth_client_id
  github_oauth_client_secret = var.github_oauth_client_secret
}