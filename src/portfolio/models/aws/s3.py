import os
import pathlib
from typing import Any, Final
import boto3
from portfolio.helpers.utils import check_if_env_vars_are_set
from portfolio.monitor.log import logger


class S3:
    client: Any
    bucket: str

    LOG = logger.bind(module="s3_module")
    TMP_FILE: Final[str] = "tmp"

    def __init__(self, bucket: str) -> None:
        check_if_env_vars_are_set(
            [
                "PORTFOLIO_S3_AWS_KEY_ID",
                "PORTFOLIO_S3_AWS_SECRET_ACCESS_KEY",
                "PORTFOLIO_S3_AWS_BUCKET",
            ]
        )

        self.bucket = bucket
        self.client = boto3.client(
            "s3",
            aws_access_key_id=os.environ.get("PORTFOLIO_S3_AWS_KEY_ID"),
            aws_secret_access_key=os.environ.get("PORTFOLIO_S3_AWS_SECRET_ACCESS_KEY"),
            region_name="eu-west-1",
        )

    def download(self, key: str, get_raw_bytes: bool = False) -> bytes | None:
        file_name: str = os.path.basename(key)

        if "." not in file_name:
            raise ValueError(f"File must have an extension: {file_name}")

        os.makedirs(self.TMP_FILE, exist_ok=True)
        if not os.path.exists(self.TMP_FILE + "/" + file_name):
            self.client.download_file(self.bucket, key, self.TMP_FILE + "/" + file_name)

        if get_raw_bytes:
            return pathlib.Path(self.TMP_FILE + "/" + file_name).read_bytes()
