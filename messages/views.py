from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from .scripts import get_messages, send_message
from contacts.scripts import wait_connection

from rest_framework.response import Response
from rest_framework import status


class messagelist(APIView):#----camel case
    #usar serializer
    def get(self, request):
        messages = get_messages(request.GET['cell'], request.GET['name'])
        return Response(messages)

    def post(self, request):
        print(request)
        send_message(request.GET['cell'], request.GET['name'], request.GET['message'])
        return Response(True, status=status.HTTP_201_CREATED)