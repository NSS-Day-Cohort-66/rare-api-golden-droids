from django.db import models

class DemotionQueue(models.Model):
    # could be BooleanField
    action = models.CharField(max_length=155)
    admin = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="initiator")
    approver_one = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="cosigner")

