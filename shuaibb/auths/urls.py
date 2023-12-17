from django.urls import (
    path,
)
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    group_list_view,
    group_detail_view,
    group_batch_delete_view,
    permission_list_view,
    permission_detail_view,
    permission_batch_delete_view,
    content_type_list_view
)

urlpatterns = [
    path("groups/", group_list_view),
    path("groups/<int:id>/", group_detail_view),
    path("groups/batchDelete/", group_batch_delete_view),
    path("permissions/", permission_list_view),
    path("permissions/<int:id>/", permission_detail_view),
    path("permissions/batchDelete/", permission_batch_delete_view),
    path("contentTypes/", content_type_list_view),
]


urlpatterns = format_suffix_patterns(urlpatterns)