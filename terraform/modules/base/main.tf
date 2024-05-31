data "azurerm_client_config" "main" {}

data "azurerm_resource_group" "main" {
    name = "Cohort28_CamBod_ProjectExercise"
}

resource "azurerm_cosmosdb_account" "db" {
	name                = "${var.prefix}-cb-todo-app-db-acc-tf"
	location            = data.azurerm_resource_group.main.location
	resource_group_name = data.azurerm_resource_group.main.name
	offer_type          = "Standard"
	kind                = "MongoDB"

	#enable_automatic_failover = true

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
		//prevent_destroy = var.prevent_db_destroy == "true" ? true : false
		prevent_destroy = false
	}

}

resource "azurerm_cosmosdb_mongo_database" "db" {
	name = var.mongo_database_name
	resource_group_name = data.azurerm_resource_group.main.name
	account_name = azurerm_cosmosdb_account.db.name
}

resource "azurerm_service_plan" "main" {
    name                = "${var.prefix}-cb-todo-app-sp-tf"
    location            = data.azurerm_resource_group.main.location
    resource_group_name = data.azurerm_resource_group.main.name
    os_type             = "Linux"
    sku_name            = "B1"
}

resource "azurerm_linux_web_app" "main" {
    name                = "${var.prefix}-${var.app_service_name}"
    location            = data.azurerm_resource_group.main.location
    resource_group_name = data.azurerm_resource_group.main.name
    service_plan_id     = azurerm_service_plan.main.id

    site_config {
        application_stack {
          docker_image_name = "cameronb9/todo-app:prod"
          docker_registry_url = "https://index.docker.io"
        }
    }

    app_settings = {
		"DOCKER_REGISTRY_SERVER_URL"          = "https://cameronb9"
		"FLASK_APP"                           = "todo_app/app"
		"FLASK_ENV"                           = "production"
		"LOGIN_DISABLED"                      = var.login_disabled
		"GITHUB_OAUTH_URL"                    = "https://github.com/login/oauth"
		"HOMEPAGE_URL"                        = "https://${var.prefix}-${var.app_service_name}.azurewebsites.net"
		"KEY_VAULT_NAME"                      = azurerm_key_vault.main.name
		"SECRET_KEY"                          = var.secret_key
		"WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
		"WEBSITES_PORT"                       = "80"
    }

	identity {
		type = "SystemAssigned"
	}
}

data azurerm_linux_web_app "main" {
	name = azurerm_linux_web_app.main.name
	resource_group_name = data.azurerm_resource_group.main.name
}

resource "azurerm_key_vault" "main" {
	name                        = "${var.prefix}-cb-todo-tf${var.key_vault_rand_str}"
	location                    = data.azurerm_resource_group.main.location
	resource_group_name         = data.azurerm_resource_group.main.name
	tenant_id                   = data.azurerm_client_config.main.tenant_id
	soft_delete_retention_days  = 7
	purge_protection_enabled    = false
	sku_name                    = "standard"
}

resource "azurerm_key_vault_access_policy" "user" {
	tenant_id = data.azurerm_client_config.main.tenant_id
	object_id = data.azurerm_client_config.main.object_id
	key_vault_id = azurerm_key_vault.main.id

	secret_permissions = ["Get", "List", "Set", "Delete", "Recover", "Purge"]
}

resource "azurerm_key_vault_access_policy" "main" {
	tenant_id    = data.azurerm_client_config.main.tenant_id
	object_id    = data.azurerm_linux_web_app.main.identity[0].principal_id
	key_vault_id = azurerm_key_vault.main.id

	secret_permissions = ["Get", "List", "Set", "Delete", "Purge"]
}



resource "azurerm_key_vault_secret" "github_oauth_client_id" {
	name = "GITHUB-OAUTH-CLIENT-ID"
	value = var.github_oauth_client_id
	key_vault_id = azurerm_key_vault.main.id
	depends_on = [ azurerm_key_vault_access_policy.user ]
}


resource "azurerm_key_vault_secret" "github_oauth_client_secret" {
	name = "GITHUB-OAUTH-CLIENT-SECRET"
	value = var.github_oauth_client_secret
	key_vault_id = azurerm_key_vault.main.id
	depends_on = [ azurerm_key_vault_access_policy.user ]
}


resource "azurerm_key_vault_secret" "mongo_connection_string" {
	name = "MONGO-CONNECTION-STRING"
	value = azurerm_cosmosdb_account.db.primary_mongodb_connection_string
	key_vault_id = azurerm_key_vault.main.id
	depends_on = [ azurerm_key_vault_access_policy.user, azurerm_cosmosdb_account.db ]
}


resource "azurerm_key_vault_secret" "mongo_database_name" {
	name = "MONGO-DATABASE-NAME"
	value = var.mongo_database_name
	key_vault_id = azurerm_key_vault.main.id
	depends_on = [ azurerm_key_vault_access_policy.user ]
}

