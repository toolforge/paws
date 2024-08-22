resource "openstack_containerinfra_cluster_v1" "k8s_127" {
  name                = "paws${var.name[var.datacenter]}-127"
  cluster_template_id = resource.openstack_containerinfra_clustertemplate_v1.template_127.id
  master_count        = 1
  node_count          = var.workers[var.datacenter]
}

resource "openstack_containerinfra_clustertemplate_v1" "template_127" {
  name                  = "paws${var.name[var.datacenter]}-127"
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
    kube_tag                  = "v1.26.8-rancher1"
    container_runtime         = "containerd"
    containerd_version        = "1.6.20"
    containerd_tarball_sha256 = "1d86b534c7bba51b78a7eeb1b67dd2ac6c0edeb01c034cc5f590d5ccd824b416"
    hyperkube_prefix          = "docker.io/rancher/"
    cloud_provider_enabled    = "true"
  }
}
