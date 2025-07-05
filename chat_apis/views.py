from django.shortcuts import render
from django.http import HttpResponse
from httplib2 import Response
# from requests import request
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from .messageMethod import *
from .authMethod import *
from .checkData import *
from rest_framework.decorators import api_view
# Create your views here.
@api_view(['GET'])
def home(request):
    return Response({"asd":"asd"})



class Webhook(APIView):

    def get(self, request):
        mode = request.query_params.get("hub.mode")
        token = request.query_params.get("hub.verify_token")
        chal = request.query_params.get("hub.challenge")
        if mode and token:
            return HttpResponse(chal)
        else:
            return HttpResponse(400)

    def post(self, request):
        data = request.data
        try:
            if data:
                changes = data['entry'][0]['changes'][0]
                field = changes['field']
                if field == 'messages':
                    value = changes['value']
                    message = value['messages'][0]
                    number = message['from']
                    message_text = message['text']['body']
                    wa_id = value['contacts'][0]['wa_id']
                    return_message = conversation(number, message_text)
                    send_message(number, return_message)
                    return HttpResponse(return_message)

                return HttpResponse(200)
            else:
                return HttpResponse(400)
        except Exception as e:
            return HttpResponse(400)



# Webhook for the FirstChatBot
class WebhookChatBot1(APIView):

    def get(self, request):
        mode = request.query_params.get("hub.mode")
        token = request.query_params.get("hub.verify_token")
        chal = request.query_params.get("hub.challenge")
        print("here get is called ")
        if mode and token:
            return HttpResponse(chal)
        else:
            return HttpResponse(400)

    def post(self, request):
        data = request.data
        try:
            if data:
                changes = data['entry'][0]['changes'][0]
                field = changes['field']
                if field == 'messages':
                    value = changes['value']
                    message = value['messages'][0]
                    number = message['from']
                    message_text = message['text']['body']
                    wa_id = value['contacts'][0]['wa_id']
                    # return_message = "Please message on +91 78199 76989 to know your TADA."
                    print(f"number : {number},  message: {message_text}")
                    return_message = conversation(number, message_text)
                    print(f"return Message  : {return_message}")
                    send_messageChatBot(number, return_message)
                    print("Message processed")
                    return HttpResponse(return_message)
                return HttpResponse(200)
            else:
                print("failed")
                return HttpResponse(400)
        except Exception as e:
            raise e
            return HttpResponse(400)




class Login(APIView):

    def get(self, request):
        return Response({"status":200})


    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(username=email, password=password)
        if user is not None:
            token = checkToken(email)
            return Response({"status":200 , "payload":token})
        else:
            return Response({"status":403 , "payload":'not ok'})

    def put(self, request):
        token = request.data.get("token")
        if token:
            status =  checkTokenValid(token)
            if status:
                return Response({"status":200, "payload":""})
        
        return Response({"status":403, "payload":""})

class EmployeeData(APIView):
    def get(self, request):
        return Response({"status":200, "payload":""})

    def post(self, request):
        token =  request.headers.get('Authorization')
        data = request.data
        if token:
            # CHECK TOKEN
            status = checkTokenValid(token)
            if status:
            # CHECK THE DATA 
            # ADD DATA
                if checkData(data):
                    return Response({"status":200, "payload":""})
                else:

                    # return Response({"status":422, "payload":data['employee_code']})
                    return Response({"status":200, "payload":""})
                    
            else:
                return Response({"status":403, "payload":""})

        else:
            return Response({"status":403, "payload":""})

@api_view(['POST'])
def mail_me_database(request):
    data = request.data
    token = data.get('tkn')
    # CREATE THE EXCEL OF THE DATABASE
    createExcel()
    # SEND MAIL TO
    sendMailWithAttachment()
    return Response({"status":200})

        



