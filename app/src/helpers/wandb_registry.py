import wandb

def publish_model(model_path, project, name, model_type="model"):
    run = wandb.init(project=project, job_type="model-publishing")
    artifact = wandb.Artifact(name, type=model_type)
    artifact.add_dir(model_path)
    run.log_artifact(artifact)
    run.finish()
    print(f"Published {name} to W&B")
