from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from users.views import (
    sign_up_view,
    login_view,
    user_by_token,
    user_list_view,
    user_detail_view
)

urlpatterns = [
    path('signup/', sign_up_view),
    path('login/', login_view),
    path('info/', user_by_token),
    path('', user_list_view),
    path('<int:id>/', user_detail_view)
]


urlpatterns = format_suffix_patterns(urlpatterns)