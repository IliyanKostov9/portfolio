from typing import Any
import os
import json
from django.contrib import messages

from django.utils.translation import gettext as _

from portfolio.models.aws.polly import Polly


def generate_text_to_speech(request: Any, LOG: Any) -> bytes | None:
    try:
        response: Any = json.loads(request.body)
        polly = Polly(os.environ.get("PORTFOLIO_S3_TEXT_TO_SPEECH_PROD_BUCKET"))

        text: str = response.get("text").strip()

        LOG.info(
            f"Received a request to perform text-to-voice for text: {text}",
        )
        stream: bytes = polly.generate(text)
        polly.close()

        return stream

    except (json.JSONDecodeError, AttributeError) as err:
        LOG.error(
            f"No text is found on the post request: {request}: {err}!",
        )
        messages.error(
            request,
            _("Application error! Sorry for the inconvenience!"),
        )

        return None
