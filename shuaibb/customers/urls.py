from django.urls import (
    path,
)
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    customer_list_view
)

urlpatterns = [
    path('', customer_list_view)
]


urlpatterns = format_suffix_patterns(urlpatterns)