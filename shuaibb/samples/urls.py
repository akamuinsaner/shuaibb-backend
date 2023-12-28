from django.urls import (
    path,
)
from rest_framework.urlpatterns import format_suffix_patterns
from samples.views import (
    sample_draft_retrive_view,
    sample_create_view,
    sample_label_list_view,
    sample_label_detail_view,
    sample_template_list_view,
    sample_template_detail_view,
    sample_list_view,
    sample_batch_delete_view,
    sample_detail_view,
    sample_label_search_view
)

urlpatterns = [
    path('list/', sample_list_view),
    path('create/', sample_create_view),
    path('batch/delete/', sample_batch_delete_view),
    path('<int:id>/', sample_detail_view),
    path('labels/', sample_label_list_view),
    path('labels/<int:id>/', sample_label_detail_view),
    path("labels/search/", sample_label_search_view),
    path('draft/retrive/', sample_draft_retrive_view),
    path('templates/', sample_template_list_view),
    path('templates/<int:id>/', sample_template_detail_view)
]


urlpatterns = format_suffix_patterns(urlpatterns)