from rest_framework import serializers
from .models import DocumentAnalysis


class DocumentAnalysisSerializer(serializers.ModelSerializer):
    document_url = serializers.SerializerMethodField()

    class Meta:
        model = DocumentAnalysis
        fields = [
            'id', 'document', 'document_url', 'original_filename', 'uploaded_at',
            'status', 'cable_category', 'voltage_rating', 'current_rating',
            'material', 'top_terms', 'extracted_specs', 'validation_errors',
            'processing_time',
        ]
        read_only_fields = [
            'id', 'uploaded_at', 'original_filename', 'status', 'cable_category',
            'voltage_rating', 'current_rating', 'material', 'top_terms',
            'extracted_specs', 'validation_errors', 'processing_time',
        ]

    def get_document_url(self, obj):
        request = self.context.get('request')
        if obj.document and request:
            return request.build_absolute_uri(obj.document.url)
        return None


class KeywordsSerializer(serializers.ModelSerializer):
    """Serializer مصغر للـ keywords endpoint"""
    class Meta:
        model = DocumentAnalysis
        fields = ['id', 'cable_category', 'top_terms', 'extracted_specs']
