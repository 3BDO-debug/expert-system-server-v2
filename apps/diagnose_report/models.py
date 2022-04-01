from django.db import models
from quiz.models import Question

# Create your models here.


class DiagnoseReport(models.Model):
    user_id = models.CharField(max_length=350, verbose_name="User ID")
    stage = models.CharField(max_length=350, verbose_name="Stage", default="G1")
    question_index = models.IntegerField(verbose_name="question index", default=0)
    pre_diagnose = models.TextField(verbose_name="Pre diagnose", null=True, blank=True)
    final_diagnose = models.TextField(verbose_name="", null=True, blank=True)

    class Meta:
        verbose_name = "Diagnose report"
        verbose_name_plural = "Diagnosis reports"

    def __str__(self):
        return f"report-{self.id} for {self.user_id}"


class DiagnoseResult(models.Model):
    diagnose_report = models.ForeignKey(
        DiagnoseReport, on_delete=models.CASCADE, verbose_name="Diagnose report"
    )
    diagnose_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    diagnose_answer = models.CharField(max_length=350, verbose_name="Diagnose answer")

    class Meta:
        verbose_name = "Diagnose result"
        verbose_name_plural = "Diagnose results"

    def __str__(self):
        return f"R-{self.diagnose_report.id} Q-{self.diagnose_question.id} ANS-{self.diagnose_answer}"
