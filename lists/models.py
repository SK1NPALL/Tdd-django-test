from django.db import models

# Create your models here.

class List(models.Model):
    pass

class Item(models.Model):
    text = models.TextField(default="")
    priority = models.CharField(max_length=255 , default="")
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)