from django.db import models
from django.contrib.auth.models import User  # to link documents to users

# 1️ Engineering Catalog
class CableStandard(models.Model):
    name = models.CharField(max_length=100)
    voltage_rating = models.FloatField()
    conductor_material = models.CharField(max_length=50)
    insulation_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# 2️ Vision Results linked to CableStandard
class CableInspection(models.Model):
    cable = models.ForeignKey(CableStandard, on_delete=models.CASCADE, related_name="inspections")
    result_image = models.ImageField(upload_to="inspection_images/")
    defect_detected = models.BooleanField(default=False)
    inspected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inspection for {self.cable.name}"

# 3️ OCR Records linked to Users
class DocumentAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="documents")
    document_file = models.FileField(upload_to="documents/")
    ocr_text = models.TextField()
    analyzed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document by {self.user.username}"

