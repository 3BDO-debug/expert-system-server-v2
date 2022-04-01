from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers
from diagnose_report import (
    models as diagnose_report_models,
    handlers as diagnose_report_handlers,
)


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def questions_handler(request):
    diagnose_report_id = request.GET.get("diagnoseReportId")
    diagnose_report = diagnose_report_models.DiagnoseReport.objects.get(
        id=int(diagnose_report_id)
    )
    group = models.Group.objects.get(group_name=diagnose_report.stage)
    questions = list(models.Question.objects.filter(group=group))

    question_serializer = serializers.QuestionSerializer(
        questions[diagnose_report.question_index], many=False
    )
    return Response(data=question_serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def answers_handler(request):
    diagnose_report_id = request.data.get("diagnoseReportId")
    diagnose_report = diagnose_report_models.DiagnoseReport.objects.get(
        id=int(diagnose_report_id)
    )
    group = models.Group.objects.get(group_name=diagnose_report.stage)
    questions = list(models.Question.objects.filter(group=group))
    question_id = request.data.get("questionId")
    answer = request.data.get("answer")

    if request.data.get("height") and request.data.get("weight"):
        height = int(request.data.get("height")) / 100
        weight = int(request.data.get("weight"))
        bmi = weight / (height**2)
        if float(bmi) <= 24.9:
            answer = "no"
        elif float(bmi) > 25 and float(bmi) <= 39.9:
            answer = "yes"

    if diagnose_report_handlers.should_i_skip(diagnose_report.stage):

        if answer == "yes":

            diagnose_report_handlers.diagnose_report_updater(
                diagnose_report=diagnose_report,
                all_no=False,
            )

        elif answer == "no":

            if diagnose_report.question_index + 1 < len(questions):

                diagnose_report.question_index += 1
                diagnose_report.save()

            else:
                diagnose_report_handlers.diagnose_report_updater(
                    diagnose_report=diagnose_report,
                    all_no=True,
                )

    elif not diagnose_report_handlers.should_i_skip(diagnose_report.stage):

        diagnose_report_handlers.results_tracker(
            diagnose_report=diagnose_report, answer=answer, question_id=question_id
        )

    return Response(status=status.HTTP_201_CREATED)
