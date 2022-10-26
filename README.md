# Kubeflow pipeline 

This is a sample pipeline that demonstrates how to perform topic modeling using [Kubeflow Pipelines](https://www.kubeflow.org/docs/pipelines/overview/pipelines-overview/).

Video for introduction: 
* https://www.youtube.com/watch?v=90hPRXiBn4U
* https://www.youtube.com/watch?v=gd7mr1G-4U0&t=1151s

## Prerequisites
* kubectl
* Cluster (Minikube, docker desktop, ...)

## Install Kubeflow pipeline - local 

```shell
export PIPELINE_VERSION=1.8.5
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic-pns?ref=$PIPELINE_VERSION"
```

See if it's running correctly 
```shell
kubectl get pods -A 
```

### Port-forward 
```shell
kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80
```
Goto -> http://localhost:8080

![](img/home.png)


## Pipeline:

* There is two ways to create a pipeline: 
    * Using Python functions 
      * Example: [old_pipeline.py](old_pipeline.py)
    * Using Docker images 
      * Example: [kubeflow](kubeflow)
***
* Two ways to run a pipeline:
  * Upload .yaml file
    * Example: [pipeline_topic_modeling.yaml](kubeflow/pipeline_topic_modeling.yaml)
  * Run via kubeflow SDK - client 
    * Example: [pipeline.py](kubeflow/pipeline.py)

*** 

Here are some ressources to get started with Kubeflow pipeline:
* https://medium.com/@gkkarobia/kubeflow-pipelines-part-1-lightweight-components-a4a3c8cb3f2d
* https://towardsdatascience.com/tutorial-basic-kubeflow-pipeline-from-scratch-5f0350dc1905
* https://github.com/kubeflow/pipelines/blob/master/samples/tutorials/Data%20passing%20in%20python%20components.ipynb
* https://github.com/kubeflow/examples/tree/master/pipelines/mnist-pipelines


### Delete Kubeflow pipeline - local 
```
export PIPELINE_VERSION=1.8.5
kubectl delete -k "github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic-pns?ref=$PIPELINE_VERSION"
kubectl delete -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
```


***

## Install Kubeflow pipeline for Apple Silicon M1
https://medium.com/@fmind/how-to-install-kubeflow-on-apple-silicon-3565db8773f3
```shell
KFP_PLATFORM=platform-agnostic-emissary
KFP_VERSION=2.0.0b4
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$KFP_VERSION"
kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/$KFP_PLATFORM?ref=$KFP_VERSION"
```

```shell
kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80
```

```shell
kubectl delete -k "github.com/kubeflow/pipelines/manifests/kustomize/env/$KFP_PLATFORM?ref=$KFP_VERSION"
kubectl delete -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$KFP_VERSION"
```