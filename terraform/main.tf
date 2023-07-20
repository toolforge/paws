terraform {
  required_version = ">= 1.5.3"
  required_providers {
    openstack = {
      source  = "terraform-provider-openstack/openstack"
      version = "~> 1.51.0"
    }
  }
}

provider "openstack" {
  auth_url                      = var.auth-url[var.datacenter]
  tenant_id                     = var.tenant_id[var.datacenter]
  application_credential_id     = var.application_credential_id[var.datacenter]
  application_credential_secret = var.application_credential_secret[var.datacenter]
}
