import os
from pathlib import Path
from typing import Any, Final
import boto3
from portfolio.helpers.utils import check_if_env_vars_are_set
from portfolio.monitor.log import logger
from botocore.exceptions import ClientError

REGION: Final[str] = "eu-west-1"


class S3:
    client: Any
    bucket: str

    LOG = logger.bind(module="s3_module")
    TMP_FILE: Final[str] = "tmp"

    def __init__(self, bucket: str) -> None:
        check_if_env_vars_are_set(
            [
                "PORTFOLIO_S3_MAIN_PROD_ACCESS_KEY_ID",
                "PORTFOLIO_S3_MAIN_PROD_SECRET_ACESS_KEY",
            ]
        )

        self.bucket = bucket
        self.client = boto3.client(
            "s3",
            aws_access_key_id=os.environ.get("PORTFOLIO_S3_MAIN_PROD_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get(
                "PORTFOLIO_S3_MAIN_PROD_SECRET_ACESS_KEY"
            ),
            region_name=REGION,
        )

    def download(self, key: str, get_raw_bytes: bool = False) -> bytes | None:
        file_name: str = os.path.basename(key)

        if "." not in file_name:
            raise ValueError(f"File must have an extension: {file_name}")
        elif not self.exists(key):
            self.LOG.error(f"Key does not exist: {key}!")
            raise ValueError(f"Key does not exist: {key}!")

        os.makedirs(self.TMP_FILE, exist_ok=True)
        if not os.path.exists(self.TMP_FILE + "/" + file_name):
            self.client.download_file(self.bucket, key, self.TMP_FILE + "/" + file_name)

        if get_raw_bytes:
            return Path(self.TMP_FILE + "/" + file_name).read_bytes()

    def upload(self, key: str, *, content: str = "", file: str = "") -> None:

        if content:
            self.client.put_object(Bucket=self.bucket, Key=key, Body=content)
        elif file:
            self.client.upload_file(file, self.bucket, key)

    def exists(self, key: str) -> bool:
        try:
            self.client.head_object(Bucket=self.bucket, Key=key)
            return True
        except ClientError as err:
            if err.response["Error"]["Code"] == "404":
                self.LOG.error(f"Key not found: {key} in bucket: {self.bucket}")
                return False
            raise
