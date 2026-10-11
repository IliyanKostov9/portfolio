import os
from pathlib import Path
from typing import Final
from unittest import TestCase
from unittest.mock import patch

import boto3
from django.utils.translation import override
from moto import mock_aws

from portfolio.models.aws.polly import Polly
from portfolio.models.aws.s3 import S3


@patch.dict(
    os.environ,
    {
        "PORTFOLIO_S3_TEXT_TO_SPEECH_PROD_ACCESS_KEY_ID": "123",
        "PORTFOLIO_S3_TEXT_TO_SPEECH_PROD_SECRET_ACCESS_KEY": "123",
    },
)
@mock_aws
class TestPolly(TestCase):
    BUCKET: Final[str] = "bucket123"

    def setUp(self) -> None:
        client_bucket = boto3.resource("s3", region_name="us-east-1")
        client_bucket.create_bucket(Bucket=self.BUCKET)

    def test_envs(self) -> None:
        with (
            patch.dict(
                os.environ,
                {
                    "PORTFOLIO_S3_TEXT_TO_SPEECH_PROD_ACCESS_KEY_ID": "",
                    "PORTFOLIO_S3_TEXT_TO_SPEECH_PROD_SECRET_ACCESS_KEY": "",
                },
            ),
            self.assertRaises(ValueError),
        ):
            Polly(self.BUCKET)

        Polly(self.BUCKET)

    def test_generate(self) -> None:
        polly = Polly(self.BUCKET)
        stream: bytes = polly.generate("This is a test")

        matches: list[str] = [
            file
            for file in os.listdir(
                str(Path(__file__).resolve().parents[5]) + "/" + S3.TMP_FILE
            )
            if file.endswith("mp3")
        ]

        self.assertIsInstance(stream, bytes)
        self.assertTrue(matches)

        language_configs = {
            "en": {
                "language_code": "en-US",
                "voice": "Joanna",
                "engine": "neural",
            },
            "fr": {
                "language_code": "fr-FR",
                "voice": "Lea",
                "engine": "neural",
            },
            "de": {
                "language_code": "de-DE",
                "voice": "Vicki",
                "engine": "neural",
            },
            "bg": {
                "language_code": "ru-RU",
                "voice": "Tatyana",
                "engine": "standard",
            },
            "blablabla": {
                "language_code": "arb",
                "voice": "Joanna",
                "engine": "neural",
            },
        }
        langs = ["en", "fr", "de", "bg", "blablabla"]

        for lang in langs:
            with override(lang):
                polly = Polly(self.BUCKET)
                config = language_configs[lang]

                self.assertEqual(polly.language_code, config["language_code"])
                self.assertEqual(polly.voice, config["voice"])
                self.assertEqual(polly.engine, config["engine"])
