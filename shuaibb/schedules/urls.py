from django.urls import (
    path,
)
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    schedule_list_view
)

urlpatterns = [
    path('', schedule_list_view)
]


urlpatterns = format_suffix_patterns(urlpatterns)