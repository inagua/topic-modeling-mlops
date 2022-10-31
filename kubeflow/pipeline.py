import kfp
from kfp import dsl
import pandas as pd


def preprocess_input_text_op(paragraph):
    return dsl.ContainerOp(
        name='preprocess_input_text',
        image='thekenken/preprocess_input_text:latest',
        command=['python', './preprocess_input_text.py'],
        arguments=['--paragraph', paragraph],
        file_outputs={
            'paragraph': '/app/paragraph.csv',
        }
    )


def embedding_op(text):
    return dsl.ContainerOp(
        name='embedding',
        image='thekenken/embedding:latest',
        command=['python', './embeddings.py'],
        arguments=['--paragraph', text],
        file_outputs={
            'embeddings': '/app/embedding.npy',
        }
    )


# embedding_op.output
def pca_dimension_reduction_op(embeddings):
    return dsl.ContainerOp(
        name='pca_dimension_reduction',
        image='thekenken/pca:latest',
        command=['python', './pca.py'],
        arguments=['--embeddings', embeddings],
        file_outputs={
            'pca_result': '/app/pca_result.npy',
        }
    )


def find_optimal_k_cluster_op(pca_result):
    return dsl.ContainerOp(
        name='find_optimal_k_cluster',
        image='thekenken/find_optimal_number_of_clusters:latest',
        command=['python', './find_optimal_k_cluster.py'],
        arguments=['--pca_result', pca_result],
        file_outputs={
            'optimal_k_cluster': '/app/optimal_k_cluster.npy',
        }
    )


def kmeans_op(n_clusters_optimal, pca_result):
    return dsl.ContainerOp(
        name='kmeans',
        image='thekenken/kmeans:latest',
        command=['python', './kmeans.py'],
        arguments=['--n_clusters_optimal', n_clusters_optimal,
                   '--pca_result', pca_result],
        file_outputs={
            'top_nearest_indices_by_clusters': '/app/top_nearest_indices_by_clusters.npy',
        }
    )


def create_dataframe_op(top_nearest_indices_by_clusters, text):
    return dsl.ContainerOp(
        name='create_dataframe_from_top_nearest_indices_by_clusters',
        image='thekenken/create_df_from_top_nearest_indices:latest',
        command=['python', './create_df.py'],
        arguments=['--top_nearest_indices_by_clusters', top_nearest_indices_by_clusters,
                   '--text', text],
        file_outputs={
            'documents': '/app/documents.csv',
        }
    )


def preprocess_documents_op(documents_path):
    return dsl.ContainerOp(
        name='preprocess_documents',
        image='thekenken/preprocess_documents:latest',
        command=['python', './preprocess_documents.py'],
        arguments=["--documents_path", documents_path],
        file_outputs={
            'documents': '/app/documents.txt',
        }
    )


def tf_idf_op(documents_path):
    return dsl.ContainerOp(
        name='TF-IDF',
        image='thekenken/tf_idf:latest',
        command=['python', './tf_idf.py'],
        arguments=["--documents_path", documents_path],
        file_outputs={
            'tf_idf': '/app/top_words.csv',
        }
    )


def generate_qcm_op(documents_path):
    return dsl.ContainerOp(
        name='Generate QCM',
        image='python:3.8',
        command=['python', './qcm.py'],
        arguments=["--documents_path", documents_path],
        file_outputs={
            'qcm': '/app/qcm.json',
        }
    )


@dsl.pipeline(
    name='Topic Modeling Pipeline',
    description='Topic Modeling Pipeline'
)
def topic_modeling_pipeline(paragraph):
    _preprocess_input_text = preprocess_input_text_op(paragraph)

    _embedding = embedding_op(dsl.InputArgumentPath(_preprocess_input_text.outputs['paragraph'])).after(
        _preprocess_input_text)

    _pca_dimension_reduction = pca_dimension_reduction_op(
        dsl.InputArgumentPath(_embedding.outputs['embeddings'])).after(_embedding)

    _find_optimal_k_cluster = find_optimal_k_cluster_op(
        dsl.InputArgumentPath(_pca_dimension_reduction.outputs['pca_result'])).after(_pca_dimension_reduction)

    _kmeans = kmeans_op(dsl.InputArgumentPath(_find_optimal_k_cluster.outputs['optimal_k_cluster']),
                        dsl.InputArgumentPath(_pca_dimension_reduction.outputs['pca_result'])).after(
        _find_optimal_k_cluster, _pca_dimension_reduction)

    _create_dataframe = create_dataframe_op(dsl.InputArgumentPath(_kmeans.outputs['top_nearest_indices_by_clusters']),
                                            dsl.InputArgumentPath(_preprocess_input_text.outputs['paragraph'])).after(
        _kmeans,
        _preprocess_input_text)

    _tf_idf = tf_idf_op(dsl.InputArgumentPath(_create_dataframe.outputs['documents'])).after(_create_dataframe)

    return _tf_idf


if __name__ == '__main__':
    # data = fetch_20newsgroups(
    #     shuffle=True,
    #     random_state=1,
    #     remove=("headers", "footers", "quotes"),
    # )
    # news_df = pd.DataFrame({'News': data.data,
    #                         'Target': data.target})
    news_df = pd.read_csv('20newgroups.csv', engine='python', encoding='utf-8')[
        "News"]  # call fetch_20newsgroups from sklearn.datasets
    print("news_df.shape", news_df.shape)
    print("news_df.head()", news_df.head())

    client = kfp.Client()
    client.create_run_from_pipeline_func(topic_modeling_pipeline, arguments={
        "paragraph": news_df})

    '''
    Run the compiler to generate the pipeline yaml file and upload it to the kubeflow pipeline
    '''
    # kfp.compiler.Compiler().compile(
    #     pipeline_func=topic_modeling_pipeline,
    #     package_path='pipeline_topic_modeling.yaml')
