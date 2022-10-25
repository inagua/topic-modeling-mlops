# Topic modeling - Kubeflow pipeline 

This is a sample pipeline that demonstrates how to perform topic modeling using [Kubeflow Pipelines](https://www.kubeflow.org/docs/pipelines/overview/pipelines-overview/).

[//]: # (## Prerequisites)

## Pipeline:

Preprocess input text -> Embedding -> PCA -> find optimal number of clusters -> K-means clustering -> create df from top nearest indices -> preprocess documents
![](../img/result.png)

## To create all images
Your docker user: 
```
export HUB_USER=thekenken
```

### To create: 
```shell
docker build -t $HUB_USER/preprocess_input_text preprocess_input_text/ && docker build -t $HUB_USER/embedding embedding/ && docker build -t $HUB_USER/pca pca/ && docker build -t $HUB_USER/find_optimal_number_of_clusters find_optimal_number_of_clusters/ && docker build -t $HUB_USER/kmeans kmeans/ && docker build -t $HUB_USER/create_df_from_top_nearest_indices create_df_from_top_nearest_indices/ && docker build -t $HUB_USER/preprocess_documents preprocess_documents/ && docker build -t $HUB_USER/tf_idf tf_idf/ && docker build -t $HUB_USER/generate_qcm generate_qcm/
```

### To push to docker hub:
https://docs.docker.com/docker-hub/repos/
```shell
docker push $HUB_USER/preprocess_input_text && docker push $HUB_USER/embedding && docker push $HUB_USER/pca && docker push $HUB_USER/find_optimal_number_of_clusters && docker push $HUB_USER/kmeans && docker push $HUB_USER/create_df_from_top_nearest_indices && docker push $HUB_USER/preprocess_documents && docker push $HUB_USER/tf_idf && docker push $HUB_USER/generate_qcm
```


## To run the pipeline:
```shell
python pipeline.py
```
