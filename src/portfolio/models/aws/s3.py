import os
from hashlib import md5
from pathlib import Path
from typing import Any, Final

import boto3
from botocore.exceptions import ClientError
from django.conf import settings

from portfolio.monitor.log import logger


class S3:
    client: Any
    bucket: str

    LOG = logger.bind(module="s3_module")
    LOCAL_TMP_DIR: Final[str] = "tmp"

    def __init__(
        self,
        bucket: str | None,
        access_key_id: str | None = None,
        secret_access_key: str | None = None,
    ) -> None:
        if bucket is None or access_key_id is None or secret_access_key is None:
            raise ValueError(
                "Variables bucket or access_key_id or secret_access_key are NOT SET!"
            )

        self.bucket = bucket
        self.client = boto3.client(
            "s3",
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name=settings.AWS_ENV,
        )

    def download(self, key: str, get_raw_bytes: bool = False) -> bytes | None:
        file_name: str = os.path.basename(key)
        local_file_path: Final[str] = self.LOCAL_TMP_DIR + "/" + file_name

        if "." not in file_name:
            raise ValueError(f"File must have an extension: {file_name}")
        elif not self.exists(key):
            self.LOG.error(f"Key does not exist: {key}!")
            raise ClientError(
                {"Error": {"Code": 404, "Message": f"Key does not exist: {key}!"}},
                "HeadObject",
            )

        os.makedirs(self.LOCAL_TMP_DIR, exist_ok=True)
        if not os.path.exists(local_file_path) or not self.is_key_eq_to_local_file(
            key, local_file_path
        ):
            self.client.download_file(self.bucket, key, local_file_path)

        if get_raw_bytes:
            return Path(local_file_path).read_bytes()

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

    def is_key_eq_to_local_file(self, key: str, local_path_path: str) -> bool:
        try:
            md5_s3_file: str = self.client.head_object(Bucket=self.bucket, Key=key)[
                "ETag"
            ][1:-1]
            md5_local_file: str = md5(Path(local_path_path).read_bytes()).hexdigest()

            return md5_s3_file == md5_local_file
        except ClientError:
            return False
