import os
from typing import Final, List
import boto3
from pathlib import Path

from django.utils.translation import override
from unittest import TestCase
from unittest.mock import patch
from portfolio.models.aws.polly import Polly
from portfolio.models.aws.s3 import S3
from moto import mock_aws


@patch.dict(
    os.environ,
    {
        "PORTFOLIO_S3_TEXT_TO_SPEECH_PROD_ACCESS_KEY_ID": "123",
        "PORTFOLIO_S3_TEXT_TO_SPEECH_PROD_SECRET_ACESS_KEY": "123",
    },
)
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
                "PORTFOLIO_S3_TEXT_TO_SPEECH_PROD_ACCESS_KEY_ID": "",
                "PORTFOLIO_S3_TEXT_TO_SPEECH_PROD_SECRET_ACESS_KEY": "",
            },
        ):
            with self.assertRaises(ValueError):
                Polly(self.BUCKET)

        Polly(self.BUCKET)

    def test_generate(self) -> None:
        polly = Polly(self.BUCKET)
        stream: bytes = polly.generate("This is a test")

        matches: List[str] = [
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
            "ge": {
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
        langs = ["en", "fr", "ge", "bg", "blablabla"]

        for lang in langs:
            with override(lang):
                polly = Polly(self.BUCKET)
                config = language_configs[lang]

                self.assertEqual(polly.language_code, config["language_code"])
                self.assertEqual(polly.voice, config["voice"])
                self.assertEqual(polly.engine, config["engine"])
