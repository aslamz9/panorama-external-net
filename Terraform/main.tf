# 1. Query Panorama for existing Shared address objects
data "external" "panorama_addresses" {
  program = ["python", "${path.module}/check_existing.py"]
}

locals {
  # Full map of all 31 desired objects: { "net_0.0.0.0_5b" = "0.0.0.0/5", ... }
  all_address_objects = {
    for cidr in var.public_ipv4_networks :
    "net_${replace(cidr, "/", "_")}b" => cidr
  }

  # Set of object names already present on Panorama
  existing_names = toset(
    compact(split(",", data.external.panorama_addresses.result.existing_names))
  )

  # Filtered map containing ONLY objects that do NOT exist yet on Panorama
  missing_address_objects = {
    for name, cidr in local.all_address_objects :
    name => cidr if !contains(local.existing_names, name)
  }
}

# 2. Create ONLY missing objects (skips entirely if all 31 already exist)
resource "panos_addresses" "public_ipv4" {
  count = length(local.missing_address_objects) > 0 ? 1 : 0

  location = {
    shared = {}
  }

  addresses = {
    for name, cidr in local.missing_address_objects : name => {
      description = "Public IPv4 network object"
      ip_netmask  = cidr
    }
  }
}

# 3. Add ALL 31 objects (both pre-existing and newly created) into External_Net
resource "panos_address_group" "external_net" {
  location = {
    shared = {}
  }

  name        = var.address_group_name
  description = "External public IPv4 networks (Excludes RFC1918)"

  static = [
    for name in keys(local.all_address_objects) : name
  ]

  depends_on = [panos_addresses.public_ipv4]
}
