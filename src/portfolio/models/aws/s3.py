import os
import pathlib
import shutil
from typing import Any
import boto3
from portfolio.helpers.utils import check_if_env_vars_are_set
from portfolio.monitor.log import logger


class S3:
    LOG = logger.bind(module="s3_module")
    client: Any
    bucket = os.environ.get("PORTFOLIO_S3_AWS_BUCKET")

    def __init__(self) -> None:
        check_if_env_vars_are_set(
            [
                "PORTFOLIO_S3_AWS_KEY_ID",
                "PORTFOLIO_S3_AWS_SECRET_ACCESS_KEY",
                "PORTFOLIO_S3_AWS_BUCKET",
            ]
        )

        self.client = boto3.client(
            "s3",
            aws_access_key_id=os.environ.get("PORTFOLIO_S3_AWS_KEY_ID"),
            aws_secret_access_key=os.environ.get("PORTFOLIO_S3_AWS_SECRET_ACCESS_KEY"),
            region_name="eu-west-1",
        )

    def download(self, key: str) -> bytes:
        file_name: str = key.split("/")[2]

        if "." not in file_name:
            raise ValueError(f"File must have an extension: {file_name}")

        os.makedirs("tmp", exist_ok=True)
        self.client.download_file(self.bucket, key, "tmp/" + file_name)
        file_obj = pathlib.Path("tmp/" + file_name).read_bytes()
        shutil.rmtree("tmp")

        return file_obj
