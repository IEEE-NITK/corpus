from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import RetrieveModelMixin

from .models import User, ExecutiveMember
from .serializers import UserSerializer, ExecutiveMemberSerializer

class UserViewSet(GenericViewSet, RetrieveModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ExecutiveMemberViewSet(ModelViewSet):
    queryset = ExecutiveMember.objects.all()
    serializer_class = ExecutiveMemberSerializer