from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from .scripts import wait_connection, get_new_messages
from login.scripts import create_new_connection
from rest_framework.response import Response
import json

class contactlist(APIView):
    def get(self, request):
        cell = request.GET['cell']
        return Response(get_new_messages(cell))
        
    def post(self, request):
        pass