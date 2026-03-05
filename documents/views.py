import time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404

from .models import DocumentAnalysis
from .serializers import DocumentAnalysisSerializer, KeywordsSerializer


ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.pdf', '.docx']


class DocumentAnalysisListView(APIView):
    """GET  /api/documents/  — كل تحليلات المستندات"""

    def get(self, request):
        docs = DocumentAnalysis.objects.all()
        serializer = DocumentAnalysisSerializer(docs, many=True, context={'request': request})
        return Response({
            'count': docs.count(),
            'results': serializer.data
        })


class DocumentAnalysisUploadView(APIView):
    """POST /api/documents/upload/  — رفع مستند وتحليله"""
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        if 'document' not in request.FILES:
            return Response({'error': 'No document file provided.'}, status=status.HTTP_400_BAD_REQUEST)

        doc_file = request.FILES['document']
        filename = doc_file.name
        ext = '.' + filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''

        if ext not in ALLOWED_EXTENSIONS:
            return Response(
                {'error': f'Unsupported file type. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        doc = DocumentAnalysis.objects.create(
            document=doc_file,
            original_filename=filename,
        )

        start_time = time.time()
        try:
            # ------------------------------------------------
            # TODO (عضو 5): استدعاء الـ OCR Engine هنا
            # from core.ocr_engine import extract_and_validate
            # specs, report = extract_and_validate(doc.document.path)
            # doc.status = report.get('status', 'ERROR')
            # doc.cable_category = specs.get('cable_category', '')
            # ...etc
            # ------------------------------------------------

            # Placeholder until OCR is connected
            doc.status = 'UNVERIFIABLE'
            doc.raw_data_note = 'OCR engine not connected yet'

        except Exception as e:
            doc.status = 'ERROR'
            doc.validation_errors = [str(e)]

        doc.processing_time = round(time.time() - start_time, 3)
        doc.save()

        serializer = DocumentAnalysisSerializer(doc, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DocumentAnalysisDetailView(APIView):
    """GET / DELETE  /api/documents/<id>/"""

    def get(self, request, pk):
        doc = get_object_or_404(DocumentAnalysis, pk=pk)
        serializer = DocumentAnalysisSerializer(doc, context={'request': request})
        return Response(serializer.data)

    def delete(self, request, pk):
        doc = get_object_or_404(DocumentAnalysis, pk=pk)
        doc.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DocumentKeywordsView(APIView):
    """GET  /api/documents/<id>/keywords/  — الكلمات المفتاحية فقط"""

    def get(self, request, pk):
        doc = get_object_or_404(DocumentAnalysis, pk=pk)
        serializer = KeywordsSerializer(doc)
        return Response(serializer.data)
