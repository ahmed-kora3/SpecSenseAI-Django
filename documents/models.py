from django.db import models


class DocumentAnalysis(models.Model):
    """OCR Module — نتائج تحليل المستندات والمواصفات"""

    STATUS_CHOICES = [
        ('READY', 'Ready for Production'),
        ('NOT_READY', 'Not Ready'),
        ('UNVERIFIABLE', 'Unverifiable'),
        ('ERROR', 'Processing Error'),
    ]

    document = models.FileField(upload_to='documents/uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    original_filename = models.CharField(max_length=255, blank=True)

    # Validation Status
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='ERROR')

    # Extracted Specs
    cable_category = models.CharField(max_length=100, blank=True)
    voltage_rating = models.CharField(max_length=50, blank=True)
    current_rating = models.CharField(max_length=50, blank=True)
    material = models.CharField(max_length=100, blank=True)

    # JSON Fields
    top_terms = models.JSONField(default=list, blank=True)
    extracted_specs = models.JSONField(default=dict, blank=True)
    validation_errors = models.JSONField(default=list, blank=True)

    processing_time = models.FloatField(null=True, blank=True, help_text="Processing time in seconds")

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Document Analysis'
        verbose_name_plural = 'Document Analyses'

    def __str__(self):
        return f"Doc #{self.pk} — {self.original_filename} [{self.status}]"
