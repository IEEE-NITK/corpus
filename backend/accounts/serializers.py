from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CorpusTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'
    
    def validate(self, attrs):
        return super().validate(attrs)