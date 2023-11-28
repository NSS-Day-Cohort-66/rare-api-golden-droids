from django.db import models

class Reaction(models.Model):
    label = models.CharField(max_length=155)
    image_url = models.URLField()