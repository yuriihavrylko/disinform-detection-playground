import uuid
from git import Optional
import kfp
import kfp.dsl as dsl
from kfp.v2.dsl import component, pipeline, Input, Output, InputPath, OutputPath, Dataset, Metrics, Model, Artifact
from kfp.client import Client

@component(
    target_image="yuriihavrylko/prjctr:latest"
)
def load(data: Output[Dataset]):
    from src.model.training import load_and_preprocess_data
    dataset = load_and_preprocess_data()

    dataset.to_csv(data.path)

@pipeline(
    name='data-loading-pipeline',
    description='A pipeline that loads and preprocesses data.'
)
def data_loading_pipeline():
    load_task = load()

def compile_pipeline() -> str:
    path = "/tmp/nlp_traininig_pipeline.yaml"
    kfp.compiler.Compiler().compile(data_loading_pipeline, path)
    return path


def create_pipeline(client: kfp.Client, namespace: str):
    print("Creating experiment")
    _ = client.create_experiment("training", namespace=namespace)

    print("Uploading pipeline")
    name = "nlp-sample-training"
    if client.get_pipeline_id(name) is not None:
        print("Pipeline exists - upload new version.")
        pipeline_prev_version = client.get_pipeline(client.get_pipeline_id(name))
        version_name = f"{name}-{uuid.uuid4()}"
        pipeline = client.upload_pipeline_version(
            pipeline_package_path=compile_pipeline(),
            pipeline_version_name=version_name,
            pipeline_id=pipeline_prev_version.id,
        )
    else:
        pipeline = client.upload_pipeline(pipeline_package_path=compile_pipeline(), pipeline_name=name)
    print(f"pipeline {pipeline.id}")


def auto_create_pipelines(
    host: str = None,
    namespace: Optional[str] = None,
):
    
    client = Client(host='<MY-KFP-ENDPOINT>')
    run = client.create_run_from_pipeline_package(
        'pipeline.yaml',
        arguments={
            'recipient': 'World',
        },
    )


if __name__ == "__main__":
    auto_create_pipelines()

