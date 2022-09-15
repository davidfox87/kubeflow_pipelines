# Installing a local deployment of Kubeflow on a local Kubernetes cluster
https://www.kubeflow.org/docs/components/pipelines/installation/localcluster-deployment/
```
kind create cluster
# env/platform-agnostic-pns hasn't been publically released, so you will install it from master
export PIPELINE_VERSION=1.8.5
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic-pns?ref=$PIPELINE_VERSION"
```

Verify that the Kubeflow Pipelines UI is accessible by port-forwarding:
```kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80```

To allow the pipelines components to pull image from docker registries:
```kubectl create secret docker-registry --namespace=kubeflow docker-hub-account --docker-server=https://docker.io --docker-username=foxy7887 --docker-password="*******!"```

and then set the secret in the kubeflow pipeline

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