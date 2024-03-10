from django.urls import path,include
from rest_framework.routers import DefaultRouter
from Spamchan.views import *

router=DefaultRouter()

router.register('report', ReportModelViewset, basename='report')

app = 'SpamChan'
urlpatterns = [
    path('api/', include(router.urls)),
]
