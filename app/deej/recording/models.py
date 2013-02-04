from django.db import models
from django.contrib.auth.models import User


class Track(models.Model):
    name = models.CharField(max_length=1024)
    artist = models.ForeignKey(User)
    record_date = models.DateTimeField(auto_now_add=True)
    upload_date = models.DateTimeField(blank=True)
