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

    def to_representation(self, instance):
        data = super(QuestionSerializer, self).to_representation(instance)
        if instance.question_image:
            data["question_image"] = instance.question_image.url
        return data
