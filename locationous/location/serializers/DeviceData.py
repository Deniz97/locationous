from location.models import DeviceData
from rest_framework import serializers


class DeviceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceData
        fields = ["device_id", "latitude", "longitude", "speed", "timestamp"]
