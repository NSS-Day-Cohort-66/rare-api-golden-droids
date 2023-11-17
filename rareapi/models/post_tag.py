from django.db import models


class PostTag(models.Model):
    """Database model for tracking Post Tags"""
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)