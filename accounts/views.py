from django.shortcuts import render
from accounts.serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.authtoken.models import Token
from accounts import models

# Create your views here.


@api_view(
    [
        "POST",
    ]
)
def user_registartion(request):

    if request.method == "POST":
        serializer = UserSerializers(data=request.data)
        data = {}
        if serializer.is_valid():
            info = serializer.save()
            data["Responce"] = "User registration successfull"
            data["username"] = info.username
            data["email"] = info.email

            token = Token.objects.get(user=info).key
            data["token"] = token
        else:
            serializer.errors
        return Response(data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(
    [
        "POST",
    ]
)
def logout_user(request):
    request.user.auth_token.delete()
    return Response(status=status.HTTP_200_OK)
