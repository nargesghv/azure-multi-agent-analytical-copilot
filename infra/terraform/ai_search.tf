resource "azurerm_search_service" "search" {
  name                = "copilot-search"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = "standard"
}