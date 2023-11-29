from django.db import models

class Subscription(models.Model):
    # could be BooleanField
    follower = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="subscription_follower")
    author = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="subscription_author")
    created_on = models.DateField(auto_now_add=True)
    ended_on = models.DateField(null=True, blank=True)