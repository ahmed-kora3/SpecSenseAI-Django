from django.db import models


class CableInspection(models.Model):
    """Vision Module — نتائج فحص مقطع الكابل"""

    STATUS_CHOICES = [
        ('PASS', 'Pass'),
        ('FAIL', 'Fail'),
        ('ERROR', 'Error'),
    ]

    image = models.ImageField(upload_to='inspections/images/')
    result_image = models.ImageField(upload_to='inspections/results/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ERROR')
    diameter_mm = models.FloatField(null=True, blank=True)
    defect_detected = models.BooleanField(default=False)
    confidence_score = models.FloatField(null=True, blank=True)
    processing_time = models.FloatField(null=True, blank=True, help_text="Processing time in seconds")
    raw_data = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Cable Inspection'
        verbose_name_plural = 'Cable Inspections'

    def __str__(self):
        return f"Inspection #{self.pk} — {self.status} ({self.uploaded_at.strftime('%Y-%m-%d %H:%M')})"
