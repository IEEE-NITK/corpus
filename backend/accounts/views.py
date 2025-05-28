from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings
from django.core.mail import send_mail

from .models import User, ExecutiveMember
from .serializers import UserSerializer, ExecutiveMemberSerializer, PasswordResetRequestSerializer, \
    PasswordResetConfirmSerializer


class UserViewSet(GenericViewSet, RetrieveModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ExecutiveMemberViewSet(ModelViewSet):
    queryset = ExecutiveMember.objects.all()
    serializer_class = ExecutiveMemberSerializer

# Forgot Password Views
class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                user = User.objects.get(email=email)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = PasswordResetTokenGenerator().make_token(user)
                reset_url = f"{settings.FRONTEND_URL}/accounts/reset?uid={uid}&token={token}"

                send_mail(
                    "Reset Password",
                    f"Use the following link to reset your password:\n {reset_url}",
                    "corpusieeenitk@gmail.com",
                    [user.email],
                    fail_silently=False
                )
            except User.DoesNotExist:
                # Don't reveal if the email exists.
                pass

        return Response({
            "detail": "If an account with that email exists, a password reset link has been sent."
        }, status=status.HTTP_200_OK)

class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            return Response({
                "detail": "Password has been reset."
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)