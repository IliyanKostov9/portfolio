import hashlib
import os
from pathlib import Path
from typing import Any
from portfolio.helpers.utils import check_if_env_vars_are_set
import boto3

from portfolio.models.aws.s3 import S3
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

    def generate(self, text: str) -> bytes:
        """
        Convert text to speech and return the mp3 file
        """
        s3 = S3(self.bucket)

        if get_language() == "fr":
            language_code = "fr-FR"
        elif get_language() == "ge":
            language_code = "de-DE"
        elif get_language() == "en":
            language_code = "en-US"
        else:
            language_code = "arb"

        mp3_file: str = (
            hashlib.sha256(f"{language_code}_{text}".encode("utf-8")).hexdigest()
            + ".mp3"
        )

        if s3.exists(mp3_file):
            if not os.path.isfile(
                str(Path(__file__).resolve().parents[4])
                + "/"
                + s3.TMP_FILE
                + "/"
                + mp3_file
            ):
                s3.download(mp3_file)

            with open(S3.TMP_FILE + "/" + mp3_file, "rb") as file:
                stream: bytes = file.read()
        else:
            stream: bytes = self.client.synthesize_speech(
                Engine="neural",
                LanguageCode=language_code,
                OutputFormat="mp3",
                Text=text,
                TextType="text",
                VoiceId="Joanna",
            )["AudioStream"].read()

            with open(S3.TMP_FILE + "/" + mp3_file, "wb") as file:
                file.write(stream)
            s3.upload(mp3_file, file=S3.TMP_FILE + "/" + mp3_file)

            self.LOG.success(
                f"I have successfully converted text-to-speech for mp3 file: {mp3_file}",
                code=200,
            )

        return stream

    def close(self) -> None:
        self.client.close()
        self.LOG.info("Polly connection closed!")
