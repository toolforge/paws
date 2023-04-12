variable "datacenter" {
  type = string
  default = "eqiad1"
}

# connection vars
variable "auth-url" {
  type = map
  default = {
    "codfw1dev" = "https://openstack.codfw1dev.wikimediacloud.org:25000"
    "eqiad1"    = "https://openstack.eqiad1.wikimediacloud.org:25000"
  }
}
variable "tenant_id" {
  type = map
  default = {
    "codfw1dev" = "paws-dev"
    "eqiad1"    = "paws"
  }
}
variable "application_credential_id" {
  type = map
  default = {
    "codfw1dev" = "f7ef9367a65b48a4896df59a938238c1"
    "eqiad1"    = "9abb08ec748d4037992f33b1626220e2"
  }
}

# magnum vars
variable "worker_flavor" {
  type = map
  default = {
    "codfw1dev" = "g3.cores1.ram2.disk20"
    "eqiad1"    = "g3.cores8.ram32.disk20"
  }
}
variable "control_flavor" {
  type = map
  default = {
    "codfw1dev" = "g3.cores1.ram2.disk20"
    "eqiad1"    = "g3.cores2.ram4.disk20"
  }
}
variable "volume_size" {
  type = map
  default = {
    "codfw1dev" = "20"
    "eqiad1"    = "80"
  }
}
variable "external_network_id" {
  type = map
  default = {
    "codfw1dev" = "wan-transport-codfw"
    "eqiad1"    = "wan-transport-eqiad"
  }
}
variable "fixed_subnet" {
  type = map
  default = {
    "codfw1dev" = "cloud-instances2-b-codfw"
    "eqiad1"    = "lan-flat-cloudinstances2b"
  }
}
variable "fixed_network" {
  type = map
  default = {
    "codfw1dev" = "lan-flat-cloudinstances2b"
    "eqiad1"    = "cloud-instances2-b-eqiad"
  }
}
variable "image_name" {
  type = map
  default = {
    "codfw1dev" = "Fedora-CoreOS-34"
    "eqiad1"    = "magnum-fedora-coreos-34"
  }
}


# trove vars
variable "network_uuid" {
  type = map
  default = {
    "codfw1dev" = "05a5494a-184f-4d5c-9e98-77ae61c56daa" # lan-flat-cloudinstances2b
    "eqiad1"    = "7425e328-560c-4f00-8e99-706f3fb90bb4" # lan-flat-cloudinstances2b
  }
}
variable "db_flavor_uuid" {
  type = map
  default = {
    "codfw1dev" = "5b2ca632-2ea0-4007-9b40-4f84f8e2428b"
    "eqiad1"    = "55d5d90f-c5c6-44ff-bb8a-be7b077481cf"
  }
}
variable "region" {
  type = map
  default = {
    "codfw1dev" = "codfw1dev-r"
    "eqiad1"    = "eqiad1-r"
  }
}
variable "db_size" {
  type = map
  default = {
    "codfw1dev" = "1"
    "eqiad1"    = "4"
  }
}
