from hep_recommender_app.configuration import Configuration
import boto3
import os
from hep_recommender_app.recommender.model import GensimWrapper


def download_model_artifacts(config: Configuration):
    """
    Downloads model artifact from S3
    """
    model_name, model_path = config.model_artifact.split("/")[-1], config.model_artifact

    boto3_client = boto3.client(
        "s3",
        region_name=config.s3["region_name"],
        aws_access_key_id=config.s3["access_key"],
        aws_secret_access_key=config.s3["secret_key"],
    )
    boto3_client.download_file(config.s3["bucket"], model_name, model_path)


def load_model(config: Configuration):
    """
    Loads trained model from disk if available, otherwise its first downloaded from S3.
    """

    if not os.path.exists(config.model_artifact):
        download_model_artifacts(config)

    model = GensimWrapper()
    model.load(config.model_artifact)
    return model