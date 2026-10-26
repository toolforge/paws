resource "openstack_containerinfra_cluster_v1" "k8s_127d" {
  name                = "paws${var.name[var.datacenter]}-127d"
  cluster_template_id = resource.openstack_containerinfra_clustertemplate_v1.template_127d.id
  master_count        = 1
  node_count          = var.workers[var.datacenter]
}

## Pending deletion when deploying the new cluster
# resource "local_file" "kube_config" {
#   content  = resource.openstack_containerinfra_cluster_v1.k8s_127d.kubeconfig.raw_config
#   filename = "kube.config"
# }

resource "openstack_containerinfra_clustertemplate_v1" "template_127d" {
  name                  = "paws${var.name[var.datacenter]}-127d"
  coe                   = "kubernetes"
  dns_nameserver        = "8.8.8.8"
  docker_storage_driver = "overlay2"
  docker_volume_size    = var.volume_size[var.datacenter]
  external_network_id   = var.external_network_id[var.datacenter]
  fixed_subnet          = var.fixed_subnet[var.datacenter]
  fixed_network         = var.fixed_network[var.datacenter]
  # Hardcoded, will go away soon
  flavor              = "g4.cores8.ram32.disk20"
  floating_ip_enabled = "false"
  image               = "Fedora-CoreOS-38"
  keypair_id          = "paws-magnum-vm"
  # Hardcoded, will go away soon
  master_flavor  = "g4.cores2.ram4.disk20"
  network_driver = "calico"

  labels = {
    kube_tag                       = "v1.27.8-rancher2"
    container_runtime              = "containerd"
    containerd_version             = "1.6.28"
    containerd_tarball_sha256      = "f70736e52d61e5ad225f4fd21643b5ca1220013ab8b6c380434caeefb572da9b"
    cloud_provider_tag             = "v1.27.3"
    cinder_csi_plugin_tag          = "v1.27.3"
    k8s_keystone_auth_tag          = "v1.27.3"
    magnum_auto_healer_tag         = "v1.27.3"
    octavia_ingress_controller_tag = "v1.27.3"
    calico_tag                     = "v3.26.4"
  }
}
