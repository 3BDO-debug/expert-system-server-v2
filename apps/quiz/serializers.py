from rest_framework.serializers import ModelSerializer
from . import models


class GroupSerializer(ModelSerializer):
    class Meta:
        model = models.Group
        fields = "__all__"


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = models.Question
        fields = "__all__"
