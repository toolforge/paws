to get kube config file:
pulumi stack output kubeconfig --show-secrets | jq -r '.raw_config'
