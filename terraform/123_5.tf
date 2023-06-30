resource "openstack_containerinfra_cluster_v1" "k8s_123_5" {
  name                = "paws${var.name[var.datacenter]}-123-5"
  cluster_template_id = resource.openstack_containerinfra_clustertemplate_v1.template_123_5.id
  master_count        = 1
  node_count          = 1
}

resource "openstack_containerinfra_clustertemplate_v1" "template_123_5" {
  name                  = "paws${var.name[var.datacenter]}-123-5"
  coe                   = "kubernetes"
  dns_nameserver        = "8.8.8.8"
  docker_storage_driver = "overlay2"
  docker_volume_size    = "${var.volume_size[var.datacenter]}"
  external_network_id   = "${var.external_network_id[var.datacenter]}"
  fixed_subnet          = "${var.fixed_subnet[var.datacenter]}"
  fixed_network         = "${var.fixed_network[var.datacenter]}"
  flavor                = "${var.worker_flavor[var.datacenter]}"
  floating_ip_enabled   = "false"
  image                 = "${var.image_name[var.datacenter]}"
  master_flavor         = "${var.control_flavor[var.datacenter]}"
  network_driver        = "flannel"

  labels = {
    kube_tag               = "v1.23.15-rancher1-linux-amd64"
    hyperkube_prefix       = "docker.io/rancher/"
    cloud_provider_enabled = "true"
  }
}

resource "openstack_db_instance_v1" "db_123_5" {
  region    = "${var.region[var.datacenter]}"
  name      = "paws${var.name[var.datacenter]}-123-5"
  flavor_id = "${var.db_flavor_uuid[var.datacenter]}"
  size      = "${var.db_size[var.datacenter]}"

  network {
    uuid = "${var.network_uuid[var.datacenter]}"
  }

  user {
    name      = "paws${var.name[var.datacenter]}"
    host      = "%"
    password  = "${var.db_password[var.datacenter]}"
    databases = ["paws"]
  }

  database {
    name     = "paws"
  }

  datastore {
    version = "5.7.29"
    type    = "mysql"
  }
}
