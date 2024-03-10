from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'
        
        
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model=Company
        fields='__all__'
        
class FraudulentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=FraudulentUser
        fields='__all__'
        
class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model=App
        fields='__all__'
        
        
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model=Report
        fields='__all__'
