from rest_framework.serializers import ModelSerializer
from . import models


class DiagnoseReportSerializer(ModelSerializer):
    class Meta:
        model = models.DiagnoseReport
        fields = "__all__"


class DiagnoseResultSerializer(ModelSerializer):
    class Meta:
        model = models.DiagnoseResult
        fields = "__all__"
