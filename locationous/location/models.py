from django.db import models


class DeviceData(models.Model):
    id = models.AutoField(primary_key=True)
    device_id = models.CharField(max_length=50)
    timestamp = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    speed = models.FloatField()

    class Meta:
        indexes = [
            models.Index(fields=["device_id", "timestamp"]),
        ]
