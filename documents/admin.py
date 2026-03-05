from django.contrib import admin
from .models import DocumentAnalysis


@admin.register(DocumentAnalysis)
class DocumentAnalysisAdmin(admin.ModelAdmin):
    list_display = ['id', 'original_filename', 'status', 'cable_category', 'voltage_rating', 'uploaded_at']
    list_filter = ['status', 'cable_category']
    search_fields = ['original_filename', 'cable_category']
    readonly_fields = ['uploaded_at', 'processing_time', 'extracted_specs', 'validation_errors', 'top_terms']
    ordering = ['-uploaded_at']
