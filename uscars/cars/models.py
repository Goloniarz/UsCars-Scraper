from django.db import models

class Cars(models.Model):
    make = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    condition = models.CharField(max_length=255)
    link = models.URLField


# Create your models here.
