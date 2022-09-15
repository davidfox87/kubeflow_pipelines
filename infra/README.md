```
terraform init
terraform apply
```

``` 
aws eks --region $(terraform output -raw region) update-kubeconfig \
    --name $(terraform output -raw cluster_name)
```

```kubectl cluster-info```

```kubectl get nodes```

# Clean up your workspace

You have now provisioned an EKS cluster, configured kubectl, and verified that your cluster is ready to use.

```terraform destroy```
