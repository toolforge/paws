variable "datacenter" {
  type = string
  default = "eqiad1"
}

# connection vars
variable "auth-url" {
  type = map
  default = {
    "codfw1dev" = "https://openstack.codfw1dev.wikimediacloud.org:25000"
    "eqiad1"    = ""
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
    "eqiad1"    = ""
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
