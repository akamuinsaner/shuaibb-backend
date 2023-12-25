from django.shortcuts import render
from rest_framework.views import APIView
from pathlib import Path
from rest_framework.response import Response
import json
from rest_framework.status import (
    HTTP_200_OK
)
# Create your views here.

class LanguageView(APIView):
    permission_classes = []
    def get(self, request):
        f = Path(__file__).resolve().parent / 'resources/i18n.json'
        content = f.read_text(encoding="utf-8")
        return Response(json.loads(content), status=HTTP_200_OK)

language_view = LanguageView.as_view()



