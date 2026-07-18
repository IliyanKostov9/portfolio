from django.http import HttpResponse, HttpResponseBadRequest

from typing import Any
from django.views import View

from portfolio.monitor.log import logger

from portfolio.helpers.voice import generate_text_to_speech


class VoiceView(View):
    LOG = logger.bind(module="voice_view")

    def post(self, request: Any) -> HttpResponse:
        stream: bytes = generate_text_to_speech(request, self.LOG)

        if stream is None:
            return HttpResponseBadRequest()

        return HttpResponse(stream, content_type="application/octet-stream")
