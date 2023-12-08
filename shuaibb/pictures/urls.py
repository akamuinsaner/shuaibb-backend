from django.urls import (
    path,
)
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    picture_folder_list_view,
    picture_list_view,
    picture_create_view,
    picture_info_detail_view,
    picture_folder_detail_view,
    picture_and_folder_search_view,
    picture_and_folder_batch_delete_view,
    picture_and_folder_batch_move_view,
    picture_cover_view
)

urlpatterns = [
    path('search/', picture_and_folder_search_view),
    path('batchDelete/', picture_and_folder_batch_delete_view),
    path('batchMove/', picture_and_folder_batch_move_view),
    path('folders/', picture_folder_list_view),
    path('folders/<int:id>/', picture_folder_detail_view),
    path('list/', picture_list_view),
    path('cover/', picture_cover_view),
    path('create/', picture_create_view),
    path('<int:id>/', picture_info_detail_view),


]


urlpatterns = format_suffix_patterns(urlpatterns)