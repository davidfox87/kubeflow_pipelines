


# Installing a local deployment of Kubeflow on a local Kubernetes cluster
https://www.kubeflow.org/docs/components/pipelines/installation/localcluster-deployment/

create Kind k8s cluster


# Installing Kubeflow on AWS
## Prerequisites
- Kubernetes EKS AWS
- Kustomize  (version 3.2.0)
- kubectl

# Clone repositories
```
export KUBEFLOW_RELEASE_VERSION=v1.5.1
export AWS_RELEASE_VERSION=v1.5.1-aws-b1.0.1
```
Run the script to clone and set the release version
```
./install.sh
```

Install Kustomize by downloading precompiled binaries
```
wget https://github.com/kubernetes-sigs/kustomize/releases/download/v3.2.0/kustomize_3.2.0_linux_amd64
mv kustomize_3.2.0_linux_amd64 kustomize
mv kustomize /usr/local/bin
```



## install with a single command
You can install all Kubeflow official components by running the following command in the infra/kubeflow_install/kubeflow_manifests folder:

```
while ! kustomize build deployments/vanilla | kubectl apply -f -; do echo "Retrying to apply resources"; sleep 30; done

```

# Port-Forward
To get started quickly, you can access Kubeflow via port-forward. Run the following to port-forward Istio’s Ingress-Gateway to local port 8080:
```
kubectl port-forward svc/istio-ingressgateway -n istio-system 8080:80
```


# Access Kubeflow Pipelines from Jupyter notebook

In order to access Kubeflow Pipelines from Jupyter notebook, an additional per namespace (profile) manifest is required:
```
kubectl apply -f kfp-access.yaml 
```

# Configuring a notebook
https://www.kubeflow.org/docs/components/notebooks/quickstart-guide/#create-a-jupyter-notebook-server-and-add-a-notebook

# kubernetes commands
https://kubernetes.io/docs/reference/kubectl/cheatsheet/


# Get commands with basic output
```
kubectl get services                          # List all services in the namespace
kubectl get pods --all-namespaces             # List all pods in all namespaces
kubectl get pods -o wide                      # List all pods in the current namespace, with more details
kubectl get deployment my-dep                 # List a particular deployment
kubectl get pods                              # List all pods in the namespace
kubectl get pod my-pod -o yaml                # Get a pod's YAML

# Describe commands with verbose output
kubectl describe nodes my-node
kubectl describe pods my-pod

# list current namespaces in the cluster
kubectl get namespace
kubectl get namespaces --show-labels
```



# Adding secrets to a namespace in the cluster
echo -n 'admin' | base64
echo -n '1f2d1e2e67df' | base64

create the manifest

kubectl apply -f ./secret.yaml

check that the secret was created:
``` 
kubectl get secrets 
kubectl get secrets mysecret -n ${NAMESPACE} -o jsonpath='{.data.password} | base64 --decode
```

kubectl describe secrets/mysecret

# Decoding the secret
To view the contents of the Secret you created, run the following command:

```kubectl get secret mysecret -o jsonpath='{.data}'```

decode the password using:
```echo 'MWYyZDFlMmU2N2Rm' | base64 --decode```

or 

```kubectl get secret mysecret -o jsonpath='{.data.password}' | base64 --decode```

## clean up
``` kubectl delete secret mysecret ```

