from django.urls import (
    path,
)
from rest_framework.urlpatterns import format_suffix_patterns
from static.views import (
    language_view,
    area_view
)

urlpatterns = [
    path('language/', language_view),
    path('areas/', area_view)
]


urlpatterns = format_suffix_patterns(urlpatterns)