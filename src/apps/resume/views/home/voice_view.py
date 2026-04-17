import json
import os
from django.http import HttpResponse, HttpResponseBadRequest

from django.contrib import messages
from typing import Any
from django.views import View

from django.utils.translation import gettext as _
from portfolio.monitor.log import logger

from portfolio.models.aws.polly import Polly


class VoiceView(View):
    LOG = logger.bind(module="voice_view")

    def post(self, request: Any) -> HttpResponse:
        try:
            response: Any = json.loads(request.body)
            polly = Polly(os.environ.get("PORTFOLIO_S3_AWS_POLLY_BUCKET"))
            text: str = response.get("text").strip()

            self.LOG.info(
                f"Received a request to perform text-to-voice for text: {text}",
            )
            stream: bytes = polly.generate(text)
            polly.close()

            return HttpResponse(stream, content_type="application/octet-stream")

        except json.JSONDecodeError:
            messages.error(
                request,
                _("Application error! Sorry for the inconvenience!"),
            )
            return HttpResponseBadRequest()
