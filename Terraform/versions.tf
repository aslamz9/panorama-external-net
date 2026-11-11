terraform {
  required_version = ">= 1.5.0"

  required_providers {
    panos = {
      source  = "PaloAltoNetworks/panos"
      version = "~> 2.0"
    }
  }
}

provider "panos" {
  # Automatically uses PANOS_HOSTNAME and PANOS_API_KEY environment variables
  skip_verify_certificate = true
}
