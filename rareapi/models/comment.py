from django.db import models


class Comment(models.Model):
    """Database for tracking comments"""
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)