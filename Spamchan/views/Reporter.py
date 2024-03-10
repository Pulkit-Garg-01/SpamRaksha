from rest_framework import viewsets, status
# from doc.api.serializers.group import GroupSerializer
from ..Serializers import ReporterSerializer
# from doc.models import Group
from ..models import Reporter

class ReporterViewset(viewsets.ModelViewSet):
    serializer_class= ReporterSerializer
    queryset= Reporter.objects.all()