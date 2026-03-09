import time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404

from .models import CableInspection
from .serializers import CableInspectionSerializer


class CableInspectionListView(APIView):
    """GET  /api/inspections/  — كل نتائج الفحص"""

    def get(self, request):
        inspections = CableInspection.objects.all()
        serializer = CableInspectionSerializer(inspections, many=True, context={'request': request})
        return Response({
            'count': inspections.count(),
            'results': serializer.data
        })


class CableInspectionUploadView(APIView):
    """POST /api/inspections/upload/  — رفع صورة وتحليلها بالـ AI"""
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        if 'image' not in request.FILES:
            return Response({'error': 'No image file provided.'}, status=status.HTTP_400_BAD_REQUEST)

        image_file = request.FILES['image']

        allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
        if image_file.content_type not in allowed_types:
            return Response({'error': 'Invalid file type. Only JPG and PNG allowed.'}, status=status.HTTP_400_BAD_REQUEST)

        inspection = CableInspection.objects.create(image=image_file)

        start_time = time.time()
        try:
            # ------------------------------------------------
            # TODO (TASK-09): ربط الـ Vision AI Engine هنا
            # from core.vision_engine import analyze_cable_image
            # result_img, data = analyze_cable_image(inspection.image.path)
            # inspection.status = data.get('status', 'ERROR')
            # inspection.diameter_mm = data.get('diameter_mm')
            # inspection.defect_detected = data.get('defect_detected', False)
            # inspection.confidence_score = data.get('confidence_score')
            # inspection.raw_data = data.get('raw_data', {})
            # if result_img:
            #     inspection.result_image = result_img
            # ------------------------------------------------

            # Placeholder until Vision AI is connected (TASK-09)
            inspection.status = 'PASS'
            inspection.raw_data = {'note': 'Vision AI not connected yet'}

        except Exception as e:
            inspection.status = 'ERROR'
            inspection.raw_data = {'error': str(e)}

        inspection.processing_time = round(time.time() - start_time, 3)
        inspection.save()

        serializer = CableInspectionSerializer(inspection, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CableInspectionDetailView(APIView):
    """GET / DELETE  /api/inspections/<id>/"""

    def get(self, request, pk):
        inspection = get_object_or_404(CableInspection, pk=pk)
        serializer = CableInspectionSerializer(inspection, context={'request': request})
        return Response(serializer.data)

    def delete(self, request, pk):
        inspection = get_object_or_404(CableInspection, pk=pk)
        inspection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
