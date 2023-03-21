# deploying magnum from tf doesn't work at present, when it does uncomment this
#resource "openstack_containerinfra_cluster_v1" "k8s_123" {
#  name                = "paws-123"
#  cluster_template_id = resource.openstack_containerinfra_clustertemplate_v1.template_123.id
#  master_count        = 1
#  node_count          = 1
#}

resource "openstack_containerinfra_clustertemplate_v1" "template_123" {
  name                  = "paws-123"
  image                 = "Fedora-CoreOS-34"
  external_network_id   = "${var.external_network_id[var.datacenter]}"
  fixed_subnet          = "${var.fixed_subnet[var.datacenter]}"
  fixed_network         = "${var.fixed_network[var.datacenter]}"
  coe                   = "kubernetes"
  flavor                = "${var.worker_flavor[var.datacenter]}"
  master_flavor         = "${var.control_flavor[var.datacenter]}"
  docker_volume_size    = "${var.volume_size[var.datacenter]}"
  dns_nameserver        = "8.8.8.8"
  docker_storage_driver = "overlay2"
  network_driver        = "flannel"
  floating_ip_enabled   = false

  labels = {
    kube_tag               = "v1.23.15-rancher1-linux-amd64"
    hyperkube_prefix       = "docker.io/rancher/"
    cloud_provider_enabled = "true"
  }
}
