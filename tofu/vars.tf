variable "datacenter" {
  type = string
}

# name codfw1dev artifacts with '-dev' names
variable "name" {
  type = map(any)
  default = {
    "codfw1dev" = "-dev"
    "eqiad1"    = ""
  }
}

# connection vars
variable "auth-url" {
  type = map(any)
  default = {
    "codfw1dev" = "https://openstack.codfw1dev.wikimediacloud.org:25000"
    "eqiad1"    = "https://openstack.eqiad1.wikimediacloud.org:25000"
  }
}
variable "tenant_id" {
  type = map(any)
  default = {
    "codfw1dev" = "pawsdev"
    "eqiad1"    = "paws"
  }
}
variable "application_credential_id" {
  type = map(any)
  default = {
    "codfw1dev" = "3f7f32ab28484173b127e1fb435057ff"
    "eqiad1"    = "74fa33352a4a44038e7f924324194fe5"
  }
}

# magnum vars
variable "worker_flavor" {
  type = map(any)
  default = {
    "codfw1dev" = "g3.cores1.ram2.disk20"
    "eqiad1"    = "g3.cores8.ram32.disk20"
  }
}
variable "control_flavor" {
  type = map(any)
  default = {
    "codfw1dev" = "g3.cores1.ram2.disk20"
    "eqiad1"    = "g3.cores2.ram4.disk20"
  }
}
variable "volume_size" {
  type = map(any)
  default = {
    "codfw1dev" = "20"
    "eqiad1"    = "80"
  }
}
variable "external_network_id" {
  type = map(any)
  default = {
    "codfw1dev" = "wan-transport-codfw"
    "eqiad1"    = "wan-transport-eqiad"
  }
}
variable "fixed_network" {
  type = map(any)
  default = {
    "codfw1dev" = "lan-flat-cloudinstances2b"
    "eqiad1"    = "lan-flat-cloudinstances2b"
  }
}
variable "fixed_subnet" {
  type = map(any)
  default = {
    "codfw1dev" = "cloud-instances2-b-codfw"
    "eqiad1"    = "cloud-instances2-b-eqiad"
  }
}
variable "image_name" {
  type = map(any)
  default = {
    "codfw1dev" = "Fedora-CoreOS-38"
    "eqiad1"    = "magnum-fedora-coreos-34"
  }
}
variable "workers" {
  type = map(any)
  default = {
    "codfw1dev" = "2"
    "eqiad1"    = "7"
  }
}
