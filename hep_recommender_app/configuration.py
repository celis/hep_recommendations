import os
import configparser


class Configuration:
    """
    Class for the configuration of the S3 access and the model artifact
    """

    CONFIG_FILE = "configs/config.ini"

    def __init__(self):
        self._parser = configparser.ConfigParser()
        self._parser.read(self.CONFIG_FILE)

    @property
    def s3(self):
        """
        config parameters for S3 access
        """
        if os.path.exists(self.CONFIG_FILE):
            config = self._parser["s3"]
            return {
                "region_name": config.get("region_name", ""),
                "bucket": config.get("bucket", ""),
                "access_key": config.get("access_key", ""),
                "secret_key": config.get("secret_key", ""),
            }
        else:
            return {
                "region_name": os.environ["AWS_S3_REGION"],
                "bucket": os.environ["S3_BUCKET_NAME"],
                "access_key": os.environ["AWS_ACCESS_KEY_ID"],
                "secret_key": os.environ["AWS_SECRET_ACCESS_KEY"],
            }

    @property
    def model_artifact(self):
        """
        config parameters for the model artifact
        """
        if os.path.exists(self.CONFIG_FILE):
            config = self._parser["model_artifact"]
            return config.get("path", "")
        else:
            return os.environ["MODEL_ARTIFACT_PATH"]