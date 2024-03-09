from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    installed_apps = models.ManyToManyField('App', blank=True)

    def __str__(self):
        return self.username


# class Company(models.Model)   


# class Report(models.Model):
#     reporter
   