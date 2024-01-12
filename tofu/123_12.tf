resource "openstack_containerinfra_cluster_v1" "k8s_123_12" {
  name                = "paws${var.name[var.datacenter]}-123-12"
  cluster_template_id = resource.openstack_containerinfra_clustertemplate_v1.template_123_12.id
  master_count        = 1
  node_count          = var.workers[var.datacenter]
}

resource "local_file" "kube_config" {
  content  = resource.openstack_containerinfra_cluster_v1.k8s_123_12.kubeconfig.raw_config
  filename = "kube.config"
}

resource "openstack_containerinfra_clustertemplate_v1" "template_123_12" {
  name                  = "paws${var.name[var.datacenter]}-123-12"
  coe                   = "kubernetes"
  dns_nameserver        = "8.8.8.8"
  docker_storage_driver = "overlay2"
  docker_volume_size    = var.volume_size[var.datacenter]
  external_network_id   = var.external_network_id[var.datacenter]
  fixed_subnet          = var.fixed_subnet[var.datacenter]
  fixed_network         = var.fixed_network[var.datacenter]
  flavor                = var.worker_flavor[var.datacenter]
  floating_ip_enabled   = "false"
  image                 = "Fedora-CoreOS-38"
  master_flavor         = var.control_flavor[var.datacenter]
  network_driver        = "flannel"

  labels = {
    kube_tag               = "v1.23.15-rancher1-linux-amd64"
    hyperkube_prefix       = "docker.io/rancher/"
    cloud_provider_enabled = "true"
  }
}
