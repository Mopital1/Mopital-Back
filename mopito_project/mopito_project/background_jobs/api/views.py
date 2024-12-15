from django.shortcuts import render
from mopito_project.background_jobs.tasks import send_otp_to_user, mark_missed_app
# Create your views here.
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework import status
from background_task.tasks import Task as BT


@api_view(['GET'])
def send_message_print(request):
    try:
        # register the background task
        send_otp_to_user(repeat=BT.DAILY)
        return Response({"msg": "tache enregistré avec succès"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def mark_missed_appoint(request):
    try:
        mark_missed_app(repeat=BT.DAILY)
        return Response({"msg": "tache enregistré avec succès"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
