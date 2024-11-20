from rest_framework import serializers


class DeviceDataInputSerializer(serializers.Serializer):
    device_id = serializers.IntegerField(required=True)
    latitude = serializers.FloatField(required=True)
    longitude = serializers.FloatField(required=True)
    speed = serializers.FloatField(required=True)
    timestamp = serializers.DateTimeField(required=True)

    def validate_device_id(self, value):
        # Custom validation logic for device_id (example)
        if value <= 0:
            raise serializers.ValidationError("Device ID must be a positive integer.")
        return value

    def validate_speed(self, value):
        # Custom validation logic for speed
        if value < 0:
            raise serializers.ValidationError("Speed cannot be negative.")
        return value

    def validate_latitude(self, value):
        # Custom validation logic for latitude
        if not (-90 <= value <= 90):
            raise serializers.ValidationError("Invalid latitude value")
        return value

    def validate_longitude(self, value):
        # Custom validation logic for longitude
        if not (-180 <= value <= 180):
            raise serializers.ValidationError("Invalid longitude value")
        return value
