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
    language_code: str
    voice: str
    engine: str

    def __init__(self, bucket: str) -> None:
        check_if_env_vars_are_set(
            [
                "PORTFOLIO_S3_TEXT_TO_SPEECH_PROD_ACCESS_KEY_ID",
                "PORTFOLIO_S3_TEXT_TO_SPEECH_PROD_SECRET_ACESS_KEY",
            ]
        )

        self.bucket = bucket
        self.client = boto3.client(
            "polly",
            aws_access_key_id=os.environ.get(
                "PORTFOLIO_S3_TEXT_TO_SPEECH_PROD_ACCESS_KEY_ID"
            ),
            aws_secret_access_key=os.environ.get(
                "PORTFOLIO_S3_TEXT_TO_SPEECH_PROD_SECRET_ACESS_KEY"
            ),
            region_name="eu-west-1",
        )

        if get_language() in ["bg"]:
            self.engine = "standard"
        else:
            self.engine = "neural"

        match get_language():
            case "fr":
                self.language_code = "fr-FR"
                self.voice = "Lea"

            case "ge":
                self.language_code = "de-DE"
                self.voice = "Vicki"

            case "en":
                self.language_code = "en-US"
                self.voice = "Joanna"

            case "bg":
                self.language_code = "ru-RU"  # NOTE: Bulgarian is not available
                self.voice = "Tatyana"

            case _:
                self.language_code = "arb"
                self.voice = "Joanna"

    def generate(self, text: str) -> bytes:
        """
        Convert text to speech and return the mp3 file
        """
        s3 = S3(
            self.bucket,
            os.environ.get("PORTFOLIO_S3_TEXT_TO_SPEECH_PROD_ACCESS_KEY_ID"),
            os.environ.get("PORTFOLIO_S3_TEXT_TO_SPEECH_PROD_SECRET_ACESS_KEY"),
        )

        mp3_file: str = (
            hashlib.sha256(f"{self.language_code}_{text}".encode("utf-8")).hexdigest()
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
                Engine=self.engine,
                LanguageCode=self.language_code,
                OutputFormat="mp3",
                Text=text,
                TextType="text",
                VoiceId=self.voice,
            )["AudioStream"].read()

            os.makedirs(S3.TMP_FILE, exist_ok=True)
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
