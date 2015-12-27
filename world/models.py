from django.contrib.auth.models import User
from django.db import models
from django.contrib.gis.db import models

class Park(models.Model):
    name = models.CharField(max_length=50)
    location = models.PointField()


class Dog(models.Model):
    name = models.CharField(max_length=34)
    a = models.ManyToManyField(User)
