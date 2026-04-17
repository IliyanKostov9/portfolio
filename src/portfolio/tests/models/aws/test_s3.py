from typing import Any, Final
from pathlib import Path
from unittest import TestCase
import boto3
import os
from unittest.mock import patch
from portfolio.models.aws.s3 import S3
from moto import mock_aws


@mock_aws
class TestS3(TestCase):
    BUCKET: Final[str] = "bucket123"
    client: Any

    def setUp(self) -> None:
        self.client = boto3.resource(
            "s3",
            region_name="us-east-1",
        )
        self.client.create_bucket(Bucket=self.BUCKET)

    def test_envs(self) -> None:
        with patch.dict(
            os.environ,
            {
                "PORTFOLIO_S3_AWS_KEY_ID": "",
                "PORTFOLIO_S3_AWS_SECRET_ACCESS_KEY": "",
            },
        ):
            with self.assertRaises(ValueError):
                S3(self.BUCKET)

        S3(self.BUCKET)

    def test_upload(self):
        self.setUp()

        key: str = "test.txt"
        s3 = S3(self.BUCKET)

        s3.upload(key, file=key)

        self.assertTrue(
            s3.exists(key), f"Key {key} does not exist in bucket {self.BUCKET}!"
        )

        self.assertFalse(
            s3.exists("test2.txt"),
            f"Key {key} exists in bucket {self.BUCKET}, where it shouldn't exist!",
        )

    def test_download(self):
        self.setUp()

        key: str = "test.txt"
        s3 = S3(self.BUCKET)

        with self.assertRaises(ValueError):
            s3.download("oaeaoe")
            s3.download(key)

        s3.upload(key, file=key)
        s3.download(key)

        self.assertTrue(
            os.path.isfile(
                str(Path(__file__).resolve().parents[5]) + "/" + s3.TMP_FILE + "/" + key
            )
        )
