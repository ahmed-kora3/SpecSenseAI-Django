from django.urls import path
from .views import (
    DocumentAnalysisListView,
    DocumentAnalysisUploadView,
    DocumentAnalysisDetailView,
    DocumentKeywordsView,
)

urlpatterns = [
    path('', DocumentAnalysisListView.as_view(), name='document-list'),
    path('upload/', DocumentAnalysisUploadView.as_view(), name='document-upload'),
    path('<int:pk>/', DocumentAnalysisDetailView.as_view(), name='document-detail'),
    path('<int:pk>/keywords/', DocumentKeywordsView.as_view(), name='document-keywords'),
]
