from django.urls import (
    path,
)
from rest_framework.urlpatterns import format_suffix_patterns
from samples.views import (
    sample_draft_retrive_view,
    sample_create_view,
    sample_update_view,
    sample_label_list_view,
    sample_template_list_view,
    sample_template_detail_view,
    sample_list_view,
)

urlpatterns = [
    path('list/', sample_list_view),
    path('create/', sample_create_view),
    path('update/', sample_update_view),
    path('labels/', sample_label_list_view),
    path('draft/retrive/', sample_draft_retrive_view),
    path('templates/', sample_template_list_view),
    path('templates/detail/', sample_template_detail_view)
]


urlpatterns = format_suffix_patterns(urlpatterns)