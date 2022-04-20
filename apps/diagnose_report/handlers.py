from statistics import mode
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers
from quiz import models as quiz_models


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def report_handler(request):
    user_id = request.GET.get("userId")
    diagnose_report = models.DiagnoseReport.objects.create(user_id=user_id, stage="G1")
    diagnose_report_serializer = serializers.DiagnoseReportSerializer(
        diagnose_report, many=False
    )
    return Response(data=diagnose_report_serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def diagnose_report_stage_checker(request):
    diagnose_report_id = request.GET.get("diagnoseReportId")
    diagnose_report = models.DiagnoseReport.objects.get(id=int(diagnose_report_id))
    diagnose_report_serializer = serializers.DiagnoseReportSerializer(
        diagnose_report, many=False
    )
    report_symptoms = models.DiagnoseResult.objects.filter(
        diagnose_report=diagnose_report
    )
    report_symptoms_serializer = serializers.DiagnoseResultSerializer(
        report_symptoms, many=True
    )

    if diagnose_report.stage == "terminate":
        return Response(
            data={
                "terminate_quiz": True,
                "diagnose_report_data": diagnose_report_serializer.data,
            },
            status=status.HTTP_200_OK,
        )
    else:
        return Response(
            data={
                "terminate_quiz": False,
                "diagnose_report_data": diagnose_report_serializer.data,
                "symptoms": report_symptoms_serializer.data,
            },
            status=status.HTTP_200_OK,
        )


def should_i_skip(group_name):

    skip_list = ["G1", "G2", "G5"]

    if group_name in skip_list:
        return True
    else:
        return False


def diagnose_report_updater(diagnose_report, all_no):

    # G1 conditions
    if diagnose_report.stage == "G1" and all_no:
        diagnose_report.stage = "G2"
    elif diagnose_report.stage == "G1" and not all_no:
        diagnose_report.stage = "G3(A)"

    # G2 conditions
    elif diagnose_report.stage == "G2" and all_no:
        diagnose_report.stage = "G4(A)"
    elif diagnose_report.stage == "G2" and not all_no:
        diagnose_report.stage = "G3(A)"

    # G3(A) conditions
    elif diagnose_report.stage == "G3(A)" and all_no:
        diagnose_report.stage = "G4(A)"
    elif diagnose_report.stage == "G3(A)" and not all_no:
        diagnose_report.pre_diagnose = "Patient have ankle fracture"
        diagnose_report.stage = "G3(B)"

    # G3(B) conditions
    elif diagnose_report.stage == "G3(B)":
        diagnose_report.stage = "G5"

    # G4(A) conditions
    elif diagnose_report.stage == "G4(A)" and all_no:
        diagnose_report.stage = "terminate"
        diagnose_report.final_diagnose = "Patient does not suffer from any injury"
    elif diagnose_report.stage == "G4(A)" and not all_no:
        diagnose_report.stage = "G4(B)"
        diagnose_report.pre_diagnose = "Patient suffer from ankle sprain"

    # G4(B) conditions
    elif diagnose_report.stage == "G4(B)":
        diagnose_report.stage = "G5"

    # G5 conditions
    elif diagnose_report.stage == "G5" and all_no:
        diagnose_report.final_diagnose = "Patient can use tense therapy"
        diagnose_report.stage = "terminate"
    elif diagnose_report.stage == "G5" and not all_no:
        diagnose_report.final_diagnose = "Patient can not use tense therapy"
        diagnose_report.stage = "terminate"

    diagnose_report.question_index = 0  # reset the question index
    diagnose_report.save()


def results_tracker(diagnose_report, answer, question_id):
    group = quiz_models.Group.objects.get(group_name=diagnose_report.stage)
    questions = list(quiz_models.Question.objects.filter(group=group))

    diagnose_results = list(
        models.DiagnoseResult.objects.filter(diagnose_report=diagnose_report).filter(
            diagnose_question__group=group
        )
    )

    diagnose_results_answers = [
        diagnose_answer.diagnose_answer for diagnose_answer in diagnose_results
    ]

    if diagnose_report.question_index + 1 >= len(questions):
        print("daadas")

        models.DiagnoseResult.objects.create(
            diagnose_report=diagnose_report,
            diagnose_question=quiz_models.Question.objects.get(id=int(question_id)),
            diagnose_answer=answer,
        ).save()

        if "yes" not in diagnose_results_answers and answer == "yes":
            diagnose_report_updater(diagnose_report=diagnose_report, all_no=False)

        elif "yes" in diagnose_results_answers and answer == "no":
            diagnose_report_updater(diagnose_report=diagnose_report, all_no=False)

        elif "yes" not in diagnose_results_answers and answer == "no":
            diagnose_report_updater(diagnose_report=diagnose_report, all_no=True)

        elif "yes" in diagnose_results_answers and answer == "yes":

            diagnose_report_updater(diagnose_report=diagnose_report, all_no=False)
    else:

        models.DiagnoseResult.objects.create(
            diagnose_report=diagnose_report,
            diagnose_question=quiz_models.Question.objects.get(id=int(question_id)),
            diagnose_answer=answer,
        ).save()

        diagnose_report.question_index += 1
        diagnose_report.save()

    """     if diagnose_report.question_index < len(questions):
        models.DiagnoseResult.objects.create(
            diagnose_report=diagnose_report,
            diagnose_question=quiz_models.Question.objects.get(id=int(question_id)),
            diagnose_answer=answer,
        ).save()

        diagnose_report.question_index += 1
        diagnose_report.save()

    elif diagnose_report.question_index + 1 >= len(questions):
        print("daadas")

        models.DiagnoseResult.objects.create(
            diagnose_report=diagnose_report,
            diagnose_question=quiz_models.Question.objects.get(id=int(question_id)),
            diagnose_answer=answer,
        ).save()

        if "yes" not in diagnose_results_answers and answer == "yes":
            diagnose_report_updater(diagnose_report=diagnose_report, all_no=False)

        elif "yes" in diagnose_results_answers and answer == "no":
            diagnose_report_updater(diagnose_report=diagnose_report, all_no=False)

        elif "yes" not in diagnose_results_answers and answer == "no":
            diagnose_report_updater(diagnose_report=diagnose_report, all_no=True)

        elif "yes" in diagnose_results_answers and answer == "yes":

            diagnose_report_updater(diagnose_report=diagnose_report, all_no=False) """

    print("hello", len(questions))
    print("hello2", diagnose_report.question_index)
