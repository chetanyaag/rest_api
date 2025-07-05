
from . views import *
from django.urls import path
urlpatterns = [
    path("", home, name="home"),
    path("webhook", Webhook.as_view(), name="webhook"),
    path("webhookChat", WebhookChatBot1.as_view(), name="webhook"),
    path("webhookChat1", WebhookChatBot1.as_view(), name="webhook1"),
    path("login",Login.as_view(), name="login"),
    path("employeeData", EmployeeData.as_view(), name="employeeData"),
    path("sendData", mail_me_database, name="sendData"),
]
