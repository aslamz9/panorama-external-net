output "address_group_name" {
  description = "Created Shared Address Group name"
  value       = panos_address_group.external_net.name
}

output "total_objects_in_group" {
  description = "Total number of public IPv4 objects in External_Net"
  value       = length(local.all_address_objects)
}

output "newly_created_objects" {
  description = "Number of missing objects created by Terraform"
  value       = length(local.missing_address_objects)
}
