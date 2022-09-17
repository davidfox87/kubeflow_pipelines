# Installing an AWS EKS cluster and an autoscaling Node group


- EKS Cluster: AWS managed Kubernetes cluster of master servers
- EKS Node Group and optionally update an Auto Scaling Group of Kubernetes worker nodes compatible with EKS.
- Associated VPC, Internet Gateway, Security Groups, and Subnets: Operator managed networking resources for the EKS Cluster and worker node instances
- Associated IAM Roles and Policies: Operator managed access resources for EKS and worker node instances


```
terraform init
terraform get
terraform apply
```


Run the following command to retrieve the access credentials for your cluster and configure kubectl.

``` 
aws eks --region $(terraform output -raw region) update-kubeconfig \
    --name $(terraform output -raw cluster_name)
```

Create an OIDC provider and associate it with for your EKS cluster with the following command:
```
eksctl utils associate-iam-oidc-provider --cluster $(terraform output -raw cluster_name) \
--region $(terraform output -raw region) --approve
```

First, get information about the cluster.
```
kubectl cluster-info
```

Now verify that all three worker nodes are part of the cluster.
```
kubectl get nodes
```

# Clean up your workspace

You have now provisioned an EKS cluster, configured kubectl, and verified that your cluster is ready to use.

```
terraform destroy
```



https://learn.hashicorp.com/tutorials/terraform/eks


kubectl apply -f pods/commands.yaml
kubectl get pods
kubectl logs command-demo
