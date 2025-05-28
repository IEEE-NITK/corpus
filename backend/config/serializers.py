from rest_framework.serializers import ModelSerializer

from .models import SIG, ModuleConfiguration
from .models import Society

class SIGSerializer(ModelSerializer):
    class Meta:
        model = SIG
        fields = [
            "id",
            "name",
            "about",
            "what_we_do",
            "slug"
        ]

class SocietySerializer(ModelSerializer):
    sigs = SIGSerializer(many=True, read_only=True)

    class Meta:
        model = Society
        fields = [
            "id",
            "name",
            "url",
            "image",
            "dark_image",
            "description",
            "sigs"
        ]

class ModuleConfigurationSerializer(ModelSerializer):
    class Meta:
        model = ModuleConfiguration
        fields = [
            "id",
            "module_name",
            "module_enabled",
            "module_config"
        ]