resource "openstack_containerinfra_cluster_v1" "k8s_136a" {
  name                = "paws${var.name[var.datacenter]}-136a"
  cluster_template_id = resource.openstack_containerinfra_clustertemplate_v1.template_136a.id
  master_count        = 1
  node_count          = var.workers[var.datacenter]
}

resource "local_file" "kube_config" {
  content  = resource.openstack_containerinfra_cluster_v1.k8s_136a.kubeconfig.raw_config
  filename = "kube.config"
}

resource "openstack_containerinfra_clustertemplate_v1" "template_136a" {
  name                  = "paws${var.name[var.datacenter]}-136a"
  coe                   = "kubernetes"
  dns_nameserver        = "8.8.8.8"
  docker_storage_driver = "overlay2"
  docker_volume_size    = var.volume_size[var.datacenter]
  external_network_id   = var.external_network_id[var.datacenter]
  fixed_subnet          = var.fixed_subnet[var.datacenter]
  fixed_network         = var.fixed_network[var.datacenter]
  flavor                = var.worker_flavor[var.datacenter]
  image             = "ubuntu-22.04-v1.36.5-for-magnum"
  keypair_id        = var.keypair_id[var.datacenter]
  master_lb_enabled = "true"
  master_flavor     = var.control_flavor[var.datacenter]
  network_driver    = "calico"

  labels = {
    kube_tag                      = "v1.36.4"
    container_runtime             = "containerd"
    containerd_version            = "1.6.28"
    containerd_tarball_sha256     = "f70736e52d61e5ad225f4fd21643b5ca1220013ab8b6c380434caeefb572da9b"
    master_lb_floating_ip_enabled = "false"
  }
}
