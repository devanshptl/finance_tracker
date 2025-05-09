from django.shortcuts import render
from accounts.serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.authtoken.models import Token
from accounts import models
from rest_framework.permissions import AllowAny
from accounts.tasks import send_token_email

# Create your views here.


@api_view(["POST"])
@permission_classes([AllowAny])
def user_registartion(request):
    serializer = UserSerializers(data=request.data)
    data = {}
    if serializer.is_valid():
        info = serializer.save()
        token = Token.objects.get(user=info).key

        # Send email asynchronously
        send_token_email.delay(info.email, token)

        data["Response"] = "User registration successful. Token sent to your email."
        data["username"] = info.username
        data["email"] = info.email
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
