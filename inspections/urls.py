from django.urls import path
from .views import (
    CableInspectionListView,
    CableInspectionUploadView,
    CableInspectionDetailView,
)

urlpatterns = [
    path('', CableInspectionListView.as_view(), name='inspection-list'),
    path('upload/', CableInspectionUploadView.as_view(), name='inspection-upload'),
    path('<int:pk>/', CableInspectionDetailView.as_view(), name='inspection-detail'),
]
