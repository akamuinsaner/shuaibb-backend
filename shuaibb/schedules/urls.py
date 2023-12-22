from django.urls import (
    path,
)
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    schedule_list_view,
    schedule_detail_view,
    schedule_history_view,
    schedule_search_view
)

urlpatterns = [
    path('', schedule_list_view),
    path('<int:id>/', schedule_detail_view),
    path('<int:id>/history/', schedule_history_view),
    path('search/', schedule_search_view)
]


urlpatterns = format_suffix_patterns(urlpatterns)