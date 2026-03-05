from django.contrib import admin
from .models import CableInspection


@admin.register(CableInspection)
class CableInspectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'diameter_mm', 'defect_detected', 'confidence_score', 'uploaded_at']
    list_filter = ['status', 'defect_detected']
    search_fields = ['id']
    readonly_fields = ['uploaded_at', 'processing_time', 'raw_data']
    ordering = ['-uploaded_at']
