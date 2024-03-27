from django.db import models

# Create your models here.

class Authors (models.Model):
    id = models.AutoField(primary_key = True)
    author = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)

class Stories (models.Model):
    id = models.AutoField(primary_key = True)
    headline = models.CharField(max_length=64)
    category = models.CharField(max_length=6)
    region = models.CharField(max_length=2)
    author = models.ForeignKey("Authors", on_delete=models.CASCADE)
    date = models.DateField()
    details = models.CharField(max_length=128)