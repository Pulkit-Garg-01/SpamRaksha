from django.urls import path,include
from rest_framework.routers import DefaultRouter
from Spamchan.views import *

router=DefaultRouter()

router.register('report', ReportModelViewset, basename='report')

urlpatterns = [
    path('', include(router.urls)),
    path('spam/', SpamAPIView.as_view()),
]
