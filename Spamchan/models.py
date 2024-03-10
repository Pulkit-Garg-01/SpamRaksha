from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField

# Create your models here.

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    installed_apps = models.ManyToManyField('App', blank=True)

    def __str__(self):
        return self.username

class Company(models.Model):
    company_name=models.CharField(max_length=50,blank=True, null=True)
    email=models.EmailField()
    password=models.CharField(max_length=15,blank=True, null=True)
    username=models.CharField(max_length=50, blank=True, null=True)
    
    REQUIRED_FIELDS = ['email', 'company_name', 'username']
    def __str__(self):
        return self.username  
    
class FraudulentUser(models.Model):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    spam_potent = models.FloatField(default=0.0)
    
    def __str__(self):
        return self.phone_number

class App(models.Model):
    app_name=models.CharField(max_length=50) 
    
    def __str__(self):
        return self.app_name
    
class Report(models.Model):
    reporter=models.ForeignKey(User, on_delete=models.CASCADE)
    spammer=models.ForeignKey(FraudulentUser, on_delete=models.CASCADE)
    reported_to=models.ForeignKey(Company,on_delete=models.CASCADE)
    message=RichTextField()
    