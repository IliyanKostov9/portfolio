import os
from typing import Final
from unittest.mock import patch

import boto3
from django.core.handlers.asgi import ASGIRequest
from django.test import TestCase
from moto import mock_aws

BUCKET: Final[str] = "bucket123"


@patch.dict(
    os.environ,
    {
        "PORTFOLIO_S3_TEXT_TO_SPEECH_PROD_ACCESS_KEY_ID": "123",
        "PORTFOLIO_S3_TEXT_TO_SPEECH_PROD_SECRET_ACCESS_KEY": "123",
        "PORTFOLIO_S3_TEXT_TO_SPEECH_PROD_BUCKET": BUCKET,
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
        response: ASGIRequest = self.client.post(
            "/home/voice/",
            data={
                "text": "This is a test",
            },
            content_type="application/json",
            follow=False,
        )

        self.assertEqual(response.status_code, 200)

        response: ASGIRequest = self.client.post(
            "/home/voice/",
            data={"no_text": "This should fail"},
            content_type="application/json",
            follow=False,
        )

        self.assertEqual(response.status_code, 400)
