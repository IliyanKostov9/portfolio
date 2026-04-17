from django.test import TestCase
from typing import Final
import boto3
import os
from moto import mock_aws

from unittest.mock import patch
from django.core.handlers.wsgi import WSGIRequest

BUCKET: Final[str] = "bucket123"


@patch.dict(
    os.environ,
    {
        "PORTFOLIO_S3_AWS_KEY_ID": "123",
        "PORTFOLIO_S3_AWS_SECRET_ACCESS_KEY": "123",
        "PORTFOLIO_S3_AWS_POLLY_BUCKET": BUCKET,
    },
)
@mock_aws
class VoiceTestCase(TestCase):
    def setUp(self) -> None:
        client = boto3.resource(
            "s3",
            region_name="us-east-1",
        )
        client.create_bucket(Bucket=BUCKET)

    def test_post(self):
        response: WSGIRequest = self.client.post(
            "/home/voice/",
            data={
                "text": "This is a test",
            },
            content_type="application/json",
            follow=False,
        )

        self.assertEqual(response.status_code, 200)

        response: WSGIRequest = self.client.post(
            "/home/voice/",
            data={"no_text": "This should fail"},
            content_type="application/json",
            follow=False,
        )

        self.assertEqual(response.status_code, 400)
