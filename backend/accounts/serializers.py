from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .models import User, ExecutiveMember
from config.serializers import SIGSerializer

class CorpusTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'
    
    def validate(self, attrs):
        return super().validate(attrs)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "phone_no",
            "gender",
            "profile_pic",
        ]

class ExecutiveMemberSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)
    sig = SIGSerializer(read_only=True)

    class Meta:
        model = ExecutiveMember
        fields = [
            "user",
            "sig",
            "edu_email",
            "roll_number",
            "reg_number",
            "minor_branch",
            "ieee_number",
            "ieee_email",
            "linkedin",
            "github",
            "hide_github",
            "hide_linkedin",
            "is_nep",
            "date_joined"
        ]

# Forgot Password Serializers
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=6, write_only=True)
    confirm_password = serializers.CharField(min_length=6, write_only=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords don't match")

        try:
            uid = smart_str(urlsafe_base64_decode(attrs["uid"]))
            user = User.objects.get(pk=uid)
            if not PasswordResetTokenGenerator().check_token(user, attrs["token"]):
                raise serializers.ValidationError("Token is invalid or expired.")
            user.set_password(attrs["new_password"])
            user.save()
            return {}
        except (DjangoUnicodeDecodeError, User.DoesNotExist):
            raise serializers.ValidationError("Invalid UID.")
