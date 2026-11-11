output "address_group_name" {
  description = "Created Shared Address Group name"
  value       = panos_address_group.external_net.name
}

output "total_objects_created" {
  description = "Total number of public IPv4 objects in External_Net"
  value       = length(local.address_objects)
}
