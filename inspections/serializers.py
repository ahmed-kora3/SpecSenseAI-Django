from rest_framework import serializers
from .models import CableInspection


class CableInspectionSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    result_image_url = serializers.SerializerMethodField()

    class Meta:
        model = CableInspection
        fields = [
            'id', 'image', 'image_url', 'result_image', 'result_image_url',
            'uploaded_at', 'status', 'diameter_mm', 'defect_detected',
            'confidence_score', 'processing_time', 'raw_data',
        ]
        read_only_fields = [
            'id', 'uploaded_at', 'status', 'diameter_mm', 'defect_detected',
            'confidence_score', 'processing_time', 'raw_data', 'result_image',
        ]

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

    def get_result_image_url(self, obj):
        request = self.context.get('request')
        if obj.result_image and request:
            return request.build_absolute_uri(obj.result_image.url)
        return None
