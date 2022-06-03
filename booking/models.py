from typing import Collection
from django.db import models
from accounts.models import CollectionAgent, User
from smartbin.models import SmartBin
from django.utils.timezone import now


# Create your models here.
class Booking(models.Model):
    PENDING = "Pending"
    ASSIGNED = "Assigned"
    COLLECTED = "Collected"
    VERIFIED ="Verified"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (ASSIGNED, "Assigned "),
        (COLLECTED, "Collected"),
        (VERIFIED, "Verified"),
    ]

    smartbin=models.ForeignKey(SmartBin, on_delete=models.CASCADE,null=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=False)
    created_date=models.DateTimeField(default=now)
    collection_date=models.DateField(null=True)
    collection_agent=models.ForeignKey(User, on_delete=models.CASCADE,null=True)