locals {
  # Converts "192.169.0.0/16" -> "net_192.169.0.0_16b"
  address_objects = {
    for cidr in var.public_ipv4_networks :
    "net_${replace(cidr, "/", "_")}b" => cidr
  }
}

resource "panos_addresses" "public_ipv4" {
  location = {
    shared = {}
  }

  addresses = {
    for name, cidr in local.address_objects : name => {
      description = "Public IPv4 network object"
      ip_netmask  = cidr
    }
  }
}

resource "panos_address_group" "external_net" {
  location = {
    shared = {}
  }

  name        = var.address_group_name
  description = "External public IPv4 networks (Excludes RFC1918)"

  static = [
    for name in keys(local.address_objects) : name
  ]

  depends_on = [panos_addresses.public_ipv4]
}
