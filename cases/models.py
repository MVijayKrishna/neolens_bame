
from django.db import models

class JaundiceCase(models.Model):
    image_id = models.CharField(max_length=100)
    image = models.ImageField(upload_to='jaundice_dataset/')
    ethnicity = models.CharField(max_length=50)
    condition = models.CharField(max_length=20)
    region = models.CharField(max_length=100)
    feeding_pattern = models.CharField(max_length=100, blank=True)
    sleeping_pattern = models.CharField(max_length=100, blank=True)
    stooling_pattern = models.CharField(max_length=100, blank=True)
    urine_color = models.CharField(max_length=100, blank=True)
    skin_color = models.CharField(max_length=100, blank=True)
    eye_color = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.image_id

