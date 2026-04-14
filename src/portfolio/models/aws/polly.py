import os
from typing import Any
from portfolio.helpers.utils import check_if_env_vars_are_set
import boto3

from django.utils.translation import get_language
from portfolio.monitor.log import logger


class Polly:
    LOG = logger.bind(module="polly_module")
    client: Any
    bucket: str

    def __init__(self, bucket: str) -> None:
        check_if_env_vars_are_set(
            [
                "PORTFOLIO_S3_AWS_KEY_ID",
                "PORTFOLIO_S3_AWS_SECRET_ACCESS_KEY",
                "PORTFOLIO_S3_AWS_POLLY_BUCKET",
            ]
        )

        self.bucket = bucket
        self.client = boto3.client(
            "polly",
            aws_access_key_id=os.environ.get("PORTFOLIO_S3_AWS_KEY_ID"),
            aws_secret_access_key=os.environ.get("PORTFOLIO_S3_AWS_SECRET_ACCESS_KEY"),
            region_name="eu-west-1",
        )

    def convert(self, input: str) -> str:
        """
        Convert text to speech and return the mp3 file
        """
        if get_language() == "fr":
            language_code = "fr-FR"
        elif get_language() == "ge":
            language_code = "de-DE"
        elif get_language() == "en":
            language_code = "en-US"
        else:
            language_code = "arb"

        mp3_file: str = os.path.basename(
            self.client.start_speech_synthesis_task(
                Engine="neural",
                LanguageCode=language_code,
                OutputFormat="mp3",
                OutputS3BucketName=self.bucket,
                OutputS3KeyPrefix="portfolio",
                Text=input,
                TextType="text",
                VoiceId="Joanna",
            )["SynthesisTask"]["OutputUri"]
        )

        return mp3_file

    def close(self) -> None:
        self.client.close()
        self.LOG.info("Polly connection closed!")
