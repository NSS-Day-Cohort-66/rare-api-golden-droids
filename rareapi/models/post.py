from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    rare_user = models.ForeignKey('RareUser', on_delete=models.CASCADE, related_name="posts")
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=250)
    publication_date = models.DateField(auto_now_add=True)
    # URLField or ImageField?
    image_url = models.ImageField(upload_to='rareimages', height_field=None, width_field=None, max_length=None, null=True)
    content = models.TextField()
    approved = models.BooleanField(default=True)
    tags = models.ManyToManyField("Tag", through="PostTag", related_name="posts")
    post_reaction_set = models.ManyToManyField("Reaction", through="PostReaction", related_name="posts")
