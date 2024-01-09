terraform {
  required_version = ">= 1.6.0"
  backend "s3" {
    region   = "eqiad1"
    bucket   = "paws:tofu-state"
    endpoint = "https://object.eqiad1.wikimediacloud.org"
    key      = "state/main"

    skip_region_validation      = true
    skip_credentials_validation = true
    force_path_style            = true


    ##access_key                  = "7f5dc99840424406ae1e888d21b936a7"
    #bucket                      = "tofu-state"
    #endpoint                    = "https://object.eqiad1.wikimediacloud.org"
    #key                         = "paws-state"
    #region                      = "default"
    ##secret_key                  = var.ec2_credential_secret[var.datacenter]
    #skip_credentials_validation = "true"
    #skip_region_validation      = "true"
    #use_path_style              = "true"
  }
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
