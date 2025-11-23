###########################################
# PROVIDER E AUTENTICAÇÃO
###########################################
terraform {
  required_version = ">= 1.3.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.70"
    }
  }
}

provider "azurerm" {
  features {}

  # Variáveis que o usuário definirá em terraform.tfvars
  subscription_id = var.subscription_id
  client_id       = var.client_id
  client_secret   = var.client_secret
  tenant_id       = var.tenant_id
}

###########################################
# VARIÁVEIS (PARÂMETROS)
###########################################
variable "project_name" {
  type    = string
  default = "asteroids-ml"
}

variable "location" {
  type    = string
  default = "brazilsouth"
}

variable "subscription_id" {}
variable "client_id" {}
variable "client_secret" {}
variable "tenant_id" {}

###########################################
# RESOURCE GROUP
###########################################
resource "azurerm_resource_group" "rg" {
  name     = "${var.project_name}-rg"
  location = var.location
}

###########################################
# STORAGE ACCOUNT (p/ modelos PKL ou logs)
###########################################
resource "azurerm_storage_account" "sa" {
  name                     = replace("${var.project_name}sa", "-", "")
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

###########################################
# APP SERVICE PLAN
###########################################
resource "azurerm_service_plan" "app_plan" {
  name                = "${var.project_name}-plan"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  os_type             = "Linux"
  sku_name            = "B1"  # básico e barato (R$20–25/mês)
}

###########################################
# APP SERVICE (FLASK)
###########################################
resource "azurerm_linux_web_app" "webapp" {
  name                = "${var.project_name}-api"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  service_plan_id     = azurerm_service_plan.app_plan.id

  site_config {
    application_stack {
      python_version = "3.12"
    }
  }

  app_settings = {
    "SUPABASE_URL" = "COLE_AQUI"
    "SUPABASE_KEY" = "COLE_AQUI"
  }
}

###########################################
# POSTGRESQL – equivalente ao Supabase
###########################################
resource "azurerm_postgresql_flexible_server" "postgres" {
  name                   = "${var.project_name}-pg"
  resource_group_name    = azurerm_resource_group.rg.name
  location               = azurerm_resource_group.rg.location
  version                = "15"
  administrator_login    = "adminuser"
  administrator_password = "AdminPassword123!"

  storage_mb      = 32768
  sku_name        = "B_Standard_B1ms"
  backup_retention_days = 7
}

resource "azurerm_postgresql_flexible_server_database" "db" {
  name      = "asteroidsdb"
  server_id = azurerm_postgresql_flexible_server.postgres.id
}

###########################################
# SAÍDAS (Outputs)
###########################################
output "webapp_url" {
  value = azurerm_linux_web_app.webapp.default_hostname
}

output "postgres_host" {
  value = azurerm_postgresql_flexible_server.postgres.fqdn
}

output "storage_account" {
  value = azurerm_storage_account.sa.primary_blob_endpoint
}
