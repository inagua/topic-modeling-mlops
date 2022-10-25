import kfp
import kfp.components as comp
import numpy
from numpy import ndarray
import pandas as pd


def preprocess_input_text_(text: str) -> list[str]:
    import re

    # Remove new line characters
    text = [re.sub('\s+', ' ', sent) for sent in text]
    # Remove distracting single quotes
    text = [re.sub("\'", "", sent) for sent in text]
    text = "".join(text)
    # text = str(text)
    text = text.split(".")
    output_string = [sentence for sentence in text if not int(len(sentence)) < 6]
    return output_string


def embedding(text: list[str], output_embeddings_path: comp.OutputPath(numpy)):
    import numpy as np
    import spacy
    spacy.cli.download("en_core_web_sm")
    embed = spacy.load("en_core_web_sm")
    data_list = [embed(doc).vector.reshape(1, -1) for doc in text]
    np.set_printoptions(suppress=True)
    output_embeddings = np.concatenate(data_list)
    # write output_embeddings in a file
    output_embeddings_path = "./app/embeddings.npy"
    np.save(output_embeddings_path, output_embeddings)
    # np.save('embedding.npy', output_embeddings)
    # with open(output_embeddings_path, 'w') as f:
    #     f.write(str(output_embeddings))


def pca_dimension_reduction(embeddings: comp.InputPath(ndarray), output_string: comp.OutputPath(ndarray)):
    import numpy as np
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler, LabelEncoder  # , RobustScaler, robust_scale, MinMaxScaler

    embeddings = np.load(embeddings)
    # le = LabelEncoder()
    # encoded = le.fit(embeddings)
    np.set_printoptions(suppress=True)
    embeddings = np.array(embeddings)
    # scaler = StandardScaler()
    # data_rescaled = scaler.fit_transform(embeddings)  # rescale embeddings
    # find the optimal number of components for PCA
    pca = PCA(n_components=0.95)
    result = pca.fit(embeddings)
    y = np.cumsum(result.explained_variance_ratio_)
    n_components = [index for index, value in enumerate(y) if value > 0.95][0]
    # apply PCA
    pca = PCA(n_components=n_components)
    output_pca_result = pca.fit_transform(data_rescaled)
    # write output_pca_result in a file
    np.save(output_string, output_pca_result)
    # return output_pca_result


def find_optimal_k_cluster(pca_result: comp.InputPath(ndarray)) -> int:
    from sklearn.cluster import KMeans
    from yellowbrick.cluster import KElbowVisualizer

    np.load(pca_result)
    # find the optimal number of clusters
    ks = range(2, 10)
    model = KMeans()
    visualizer = KElbowVisualizer(model, k=ks)
    visualizer.fit(pca_result)
    output_n_clusters_optimal = visualizer.elbow_value_
    return output_n_clusters_optimal


def fit_kmeans_and_find_nearest_topic_clusters(n_clusters_optimal: int, pca_result: comp.InputPath(ndarray)) -> list[int]:
    from sklearn.cluster import KMeans
    import numpy as np

    pca_result = np.load(pca_result)
    kmeans_model = KMeans(n_clusters=n_clusters_optimal, random_state=0)
    kmeans_model.fit(pca_result)
    centers = np.array(kmeans_model.cluster_centers_)

    n = 5
    top_nearest_indices_by_clusters = []
    for cluster in range(len(centers)):
        ind = np.argsort(kmeans_model.transform(pca_result)[:, cluster])[:n]
        top_nearest_indices_by_clusters.append(ind)

    return top_nearest_indices_by_clusters


# , documents: comp.OutputPath(str)
def create_dataframe_from_top_nearest_indices(top_nearest_indices_by_clusters: list[int],
                                              text: list[str], outputs_documents: comp.OutputPath(str)):
    import pandas as pd

    all_documents = []
    for cluster in top_nearest_indices_by_clusters:
        document = []
        for index in cluster:
            if int(len(text[index]) <= int(4)): continue
            text[index] = text[index] + ". "
            document.append(text[index])
        all_documents.append(document)
    courses = {
        'documents': all_documents
    }
    documents = pd.DataFrame(courses)
    with open(outputs_documents, 'w') as w:
        w.write(documents)
    # return documents

# , output_documents: comp.OutputPath(str)
def preprocess_documents_(documents: comp.InputPath(str), output_documents: comp.OutputPath(str)):
    with open(csv_path, 'r') as reader:
        documents = reader.read()
    documents = documents['documents']
    temp = []
    for i in range(len(documents)):
        temp.append("".join(documents[i]))
    documents = temp
    output_documents = " ".join(documents)
    with open("documents", 'w') as writer:
        writer.write(output_documents)
    # return output_documents


# Link to your container image
# base_img = "python:alpine3.15"  # Change to your registry's URI
base_img = "python:3.8-slim"  # Change to your registry's URI
# base_img = "test/qcm:web"  # Change to your registry's URI

# Create first OP
preprocess_input_text = kfp.components.create_component_from_func(preprocess_input_text_, base_image=base_img)

# Create second OP
embedding_data = kfp.components.create_component_from_func(embedding, base_image=base_img,
                                                           packages_to_install=["numpy", "spacy"])

# Create third OP
pca_dimension_reduction = kfp.components.create_component_from_func(pca_dimension_reduction, base_image=base_img,
                                                                    packages_to_install=["scikit-learn", "numpy"])

# Create fourth OP
find_optimal_k_cluster = kfp.components.create_component_from_func(find_optimal_k_cluster, base_image=base_img,
                                                                   packages_to_install=["scikit-learn", "yellowbrick"])

# Create fifth OP
fit_kmeans_and_find_nearest_topic_clusters = kfp.components.create_component_from_func(
    fit_kmeans_and_find_nearest_topic_clusters, base_image=base_img, packages_to_install=["scikit-learn", "numpy"])

# Create sixth OP
create_dataframe_from_top_nearest_indices = kfp.components.create_component_from_func(
    create_dataframe_from_top_nearest_indices, base_image=base_img, packages_to_install=["pandas"])

# Create seventh OP
preprocess_documents_ = kfp.components.create_component_from_func(preprocess_documents_, base_image=base_img)


@kfp.dsl.pipeline(
    name='Test pipeline - TOPIC MODELING',
    description='This is a test pipeline for topic modeling'
)
def topic_modeling_pipeline(
        paragraph,
):
    # Call the first OP
    first_task = preprocess_input_text(paragraph)

    # Call the second OP and pass it the first task's outputs
    second_task = embedding_data(first_task.outputs['output'])

    third_task = pca_dimension_reduction(second_task.outputs)

    fourth_task = find_optimal_k_cluster(third_task.outputs['output_string'])

    fifth_task = fit_kmeans_and_find_nearest_topic_clusters(fourth_task.outputs['output'],
                                                            third_task.outputs['output_string'])

    seventh_task = create_dataframe_from_top_nearest_indices(fifth_task.outputs['output'],
                                                             first_task.outputs['output'])

    eigth_task = preprocess_documents_(seventh_task.outputs['outputs_documents'])


if __name__ == '__main__':
    kfp.compiler.Compiler().compile(
        pipeline_func=topic_modeling_pipeline,
        package_path='pipeline.yaml')
