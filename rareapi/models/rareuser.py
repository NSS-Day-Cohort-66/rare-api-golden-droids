from django.db import models
from django.contrib.auth.models import User

class RareUser(models.Model):
    bio = models.CharField(max_length=155)
    profile_image_url = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=155)
    created_on = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')