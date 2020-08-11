from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from .scripts import create_new_connection
from rest_framework.response import Response

class loginlist(APIView):
    def get(self, request):
        return Response(create_new_connection(request.GET['cell']))

    def post(self, request):
        pass