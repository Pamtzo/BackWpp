from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from .scripts import create_new_connection, get_pedidos, dispatch, get_messages, get_contacts
from .scripts import replace, get_last_pedido, send_message, create_delivery, checkLog, checkNumber
from PROJECT.variables import WAIT
from rest_framework.response import Response
import json

class loginlist(APIView):
    def get(self, request):
        if request.GET['code']=='1':
            if len(request.GET['contact']) <=1:
                return Response({'messages':[]})
            if request.GET['contact'][0] == ' ' and request.GET['contact'][1].isnumeric():
                return Response(get_messages(request.GET['cellphone'],replace(request.GET['contact'])))
            return Response(get_messages(request.GET['cellphone'],request.GET['contact']))
        elif request.GET['code']=='2':
            return Response(get_pedidos(request.GET['sucursal'], request.GET['cellphone']))
        elif request.GET['code']=='3':
            return Response(get_contacts(request.GET['cellphone']))
        elif request.GET['code']=='4':
            if request.GET['contact'][0] == ' ' and request.GET['contact'][1].isnumeric():
                return Response(get_last_pedido(request.GET['cellphone'],replace(request.GET['contact'])))
            return Response(get_last_pedido(request.GET['cellphone'],request.GET['contact']))
        elif request.GET['code']=='5':
            return Response(checkLog(request.GET['user'],request.GET['password']))
        elif request.GET['code']=='6':
            return Response(checkNumber(request.GET['cellphone']))
        else:
            if checkNumber(request.GET['cellphone'])['state']:
                return Response(create_new_connection(request.GET['cellphone']))
            return Response({'state':False})

    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        if request.GET['code']=='1':
            send_message(body['cellphone'],body['contact'],body['message'])
        elif request.GET['code']=='2':
            dispatch(body['pk'], body['contact'], body['cellphone'])
        elif request.GET['code']=='3':
            create_delivery(body['form'],body['cellphone'])
        elif request.GET['code']=='4':
            pass
        return Response({})
