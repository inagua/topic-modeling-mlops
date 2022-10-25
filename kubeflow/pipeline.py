import kfp
from kfp import dsl


def preprocess_input_text_op(paragraph):
    return dsl.ContainerOp(
        name='preprocess_input_text',
        image='thekenken/preprocess_input_text:latest',
        # image='python:3.8-slim',
        # command=["python", -u, -m, "kfp_component.launcher"],
        command=['python', './preprocess_input_text.py'],
        # command=['python', './preprocess_input_text/preprocess_input_text.py'],
        arguments=['--paragraph', paragraph],
        file_outputs={
            'paragraph': '/app/paragraph.csv',
        }
    )


# preprocess_input_text_op.output
def embedding_op(text):
    return dsl.ContainerOp(
        name='embedding',
        image='thekenken/embedding:latest',
        # command=['python', './embedding/embeddings.py'],
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
        image='thekenken/generate_qcm:latest',
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
    # _embedding = embedding_op(dsl.InputArgumentPath(_preprocess_input_text.outputs))

    # _pca_dimension_reduction = pca_dimension_reduction_op(_embedding.outputs['embeddings']).after(_embedding)
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

    # _preprocess_documents = preprocess_documents_op(
    #     dsl.InputArgumentPath(_create_dataframe.outputs['documents'])).after(_create_dataframe)

    _tf_idf = tf_idf_op(dsl.InputArgumentPath(_create_dataframe.outputs['documents'])).after(_create_dataframe)

    # _generate_qcm = generate_qcm_op(dsl.InputArgumentPath(_preprocess_documents.outputs['documents'])).after(
    #     _preprocess_documents)

    return _tf_idf


if __name__ == '__main__':
    client = kfp.Client()
    client.create_run_from_pipeline_func(topic_modeling_pipeline, arguments={
        "paragraph": "The Elder Scrolls V: Skyrim is an action role-playing video game developed by Bethesda Game Studios and published by Bethesda Softworks. It is the fifth main installment in The Elder Scrolls series, following The Elder Scrolls IV: Oblivion.The game's main story revolves around the player character's quest to defeat Alduin the World-Eater, a dragon who is prophesied to destroy the world. The game is set 200 years after the events of Oblivion and takes place in the fictional province of Skyrim. Over the course of the game, the player completes quests and develops the character by improving skills. The game continues the open-world tradition of its predecessors by allowing the player to travel anywhere in the game world at any time, and to ignore or postpone the main storyline indefinitely.The team opted for a unique and more diverse open world than Oblivion's Imperial Province of Cyrodiil, which game director and executive producer Todd Howard considered less interesting by comparison. The game was released to critical acclaim, with reviewers particularly mentioning the character advancement and setting, and is considered to be one of the greatest video games of all time. "})
    # "paragraph": "Machine learning (ML) is the scientific study of algorithms and statistical models that computer systems use to progressively improve their performance on a specific task. Machine learning algorithms build a mathematical model of sample data, known as ‘training data’, in order to make predictions or decisions without being explicitly programmed to perform the task. Machine learning algorithms are used in the applications of email filtering, detection of network intruders, and computer vision, where it is infeasible to develop an algorithm of specific instructions for performing the task. Machine learning is closely related to computational statistics, which focuses on making predictions using computers. The study of mathematical optimization delivers methods, theory and application domains to the field of machine learning. Data mining is a field of study within machine learning, and focuses on exploratory data analysis through unsupervised learning.In its application across business problems, machine learning is also referred to as predictive analytics."})

    # kfp.compiler.Compiler().compile(
    #     pipeline_func=topic_modeling_pipeline,
    #     package_path='pipeline_topic_modeling.yaml')
