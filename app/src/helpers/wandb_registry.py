from pathlib import Path
import wandb

def publish_model(model_path: str, project: str, name: str, model_type: str = "model"):
    with wandb.init(project=project, job_type="model-publishing") as run:
        artifact = wandb.Artifact(name, type=model_type)
        artifact.add_dir(model_path)
        run.log_artifact(artifact)
    print(f"Published {name} to W&B")

def download_model(model_name: str, project: str, download_path: Path, model_type: str = "model"):
    with wandb.init(project=project) as run:
        artifact = run.use_artifact(model_name, type=model_type)
        artifact_dir = artifact.download(root=download_path)
        print(f"Downloaded {model_name} to {artifact_dir}")
