from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Reporter)
admin.site.register(User)
admin.site.register(FraudulentUser)
admin.site.register(App)
admin.site.register(Company)
