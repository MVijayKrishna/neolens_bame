# jaundice_insight/models.py

from django.db import models

class JaundicePrediction(models.Model):
    ethnicity = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    feeding_pattern = models.CharField(max_length=50)
    sleeping_pattern = models.CharField(max_length=50)
    stooling_pattern = models.CharField(max_length=50)
    urine_color = models.CharField(max_length=50)
    skin_color = models.CharField(max_length=50)
    eye_color = models.CharField(max_length=50)
    prediction = models.CharField(max_length=20)
    confidence = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
