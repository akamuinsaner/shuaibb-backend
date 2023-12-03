from django.urls import path
from .views import FileUploadAPIView, FileUploadCosView


urlpatterns = [
    path('common/', FileUploadAPIView.as_view()),
    path('common/cos/', FileUploadCosView.as_view()),
]