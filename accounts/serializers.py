from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializers(serializers.ModelSerializer):

    password2 = serializers.CharField(style={"input": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]
        extra_kwargs = {"password": {"write_only": True}}

    def save(self):
        pass1 = self.validated_data["password"]
        pass2 = self.validated_data["password2"]
        username = self.validated_data["username"]
        email = self.validated_data["email"]

        if pass1 != pass2:
            raise serializers.ValidationError({"error": "Password not matched "})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error": "Email already exists "})

        info = User(email=email, username=username)
        info.set_password(pass1)
        info.save()
        return info
