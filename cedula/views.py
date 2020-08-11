from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from .scripts import getdata
from rest_framework.response import Response

class cedula(APIView):
    def get(self, request):
        pass

    def post(self, request):
        return Response(getdata(request.POST['data']))