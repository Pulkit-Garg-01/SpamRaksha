from rest_framework import viewsets, status
# from doc.api.serializers.group import GroupSerializer
from Spamchan.serializers import ReportSerializer
# from doc.models import Group
from Spamchan.models import Report

class ReportModelViewset(viewsets.ModelViewSet):
    serializer_class= ReportSerializer
    queryset= Report.objects.all()
