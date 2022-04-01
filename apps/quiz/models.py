from django.db import models
from cloudinary.models import CloudinaryField


# Quiz models


class Group(models.Model):
    group_name = models.CharField(max_length=350, verbose_name="Group name")

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"

    def __str__(self):
        return self.group_name


class Question(models.Model):
    group = models.ForeignKey(Group, verbose_name="Group", on_delete=models.CASCADE)
    question_text = models.TextField(verbose_name="Question text")
    question_image = CloudinaryField(
        verbose_name="Question image", null=True, blank=True
    )
    calc_bmi = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return f"{self.group.group_name} - {self.question_text}"
