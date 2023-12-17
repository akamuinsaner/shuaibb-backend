from django.urls import (
    path,
)
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    customer_list_view,
    customer_detail_view,
    customer_batch_delete_view
)

urlpatterns = [
    path('', customer_list_view),
    path('<int:id>', customer_detail_view),
    path('batchDelete/', customer_batch_delete_view)
]


urlpatterns = format_suffix_patterns(urlpatterns)