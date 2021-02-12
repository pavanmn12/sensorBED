from rest_framework.serializers import ModelSerializer
from .models import *


class SensorDataSerializer(ModelSerializer):

    class Meta:
        model = SensorData
        fields = "__all__"