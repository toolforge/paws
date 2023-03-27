# deploying magnum from tf doesn't work at present, when it does uncomment this
#resource "openstack_containerinfra_cluster_v1" "k8s_123" {
#  name                = "paws-123"
#  cluster_template_id = resource.openstack_containerinfra_clustertemplate_v1.template_123.id
#  master_count        = 1
#  node_count          = 1
#}

resource "openstack_containerinfra_clustertemplate_v1" "template_123" {
  name                  = "paws-123"
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

resource "openstack_db_instance_v1" "db_123" {
  region    = "${var.region[var.datacenter]}"
  name      = "paws-123"
  flavor_id = "${var.db_flavor_uuid[var.datacenter]}"
  size      = "${var.db_size[var.datacenter]}"

  network {
    uuid = "${var.network_uuid[var.datacenter]}"
  }

  user {
    name      = "paws-123"
    host      = "%"
    password  = "${var.db_password[var.datacenter]}"
    databases = ["paws-123"]
  }

  database {
    name     = "paws-123"
  }

  datastore {
    version = "5.7.29"
    type    = "mysql"
  }
}
