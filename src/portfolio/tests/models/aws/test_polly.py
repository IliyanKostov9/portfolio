import os
from typing import Final
import boto3
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch
from portfolio.models.aws.polly import Polly
from portfolio.models.aws.s3 import S3
from moto import mock_aws


@mock_aws
class TestPolly(TestCase):
    BUCKET: Final[str] = "bucket123"

    def setUp(self) -> None:
        client_bucket = boto3.resource("s3", region_name="us-east-1")
        client_bucket.create_bucket(Bucket=self.BUCKET)

    def test_envs(self) -> None:
        with patch.dict(
            os.environ,
            {
                "PORTFOLIO_S3_AWS_KEY_ID": "",
                "PORTFOLIO_S3_AWS_SECRET_ACCESS_KEY": "",
            },
        ):
            with self.assertRaises(ValueError):
                Polly(self.BUCKET)

        Polly(self.BUCKET)

    def test_generate(self) -> None:
        self.setUp()

        polly = Polly(self.BUCKET)
        polly.generate("This is a test")

        self.assertTrue(
            os.path.isdir(str(Path(__file__).resolve().parents[5]) + "/" + S3.TMP_FILE)
        )
