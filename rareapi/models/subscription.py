from django.db import models

class Subscription(models.Model):
    # could be BooleanField
    follower_id = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="subscription_follower")
    author_id = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="subscription_author")
    created_on = models.DateField(auto_now_add=True)
    ended_on = models.DateField(blank=True)