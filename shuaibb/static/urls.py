from django.urls import (
    path,
)
from rest_framework.urlpatterns import format_suffix_patterns
from static.views import (
    language_view
)

urlpatterns = [
    path('language/', language_view),
]


urlpatterns = format_suffix_patterns(urlpatterns)