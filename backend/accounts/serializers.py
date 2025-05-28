from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User, ExecutiveMember
from config.serializers import SIGSerializer

class CorpusTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'
    
    def validate(self, attrs):
        return super().validate(attrs)

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "phone_no",
            "gender",
            "profile_pic",
        ]

class ExecutiveMemberSerializer(HyperlinkedModelSerializer):
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