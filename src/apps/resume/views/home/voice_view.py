from django.http import HttpResponse
from typing import Any
from django.views import View

from portfolio.monitor.log import logger

from portfolio.models.aws.polly import Polly


class VoiceView(View):
    LOG = logger.bind(module="voice_view")

    def post(self, request: Any) -> HttpResponse:
        polly = Polly()
        polly.start("test")

        return HttpResponse()
