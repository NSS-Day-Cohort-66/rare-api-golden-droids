from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    rare_user = models.ForeignKey('RareUser', on_delete=models.CASCADE, related_name="posts")
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=250)
    publication_date = models.DateField(auto_now_add=True)
    image_url = models.URLField()
    content = models.TextField()
    approved = models.BooleanField(default=True)