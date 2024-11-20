from django.test import tag
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from location.models import DeviceData


@tag("integration-test")
class DeviceDataAPITestCase(APITestCase):

    def setUp(self):
        # Create any required initial data here, if necessary
        self.device_data = DeviceData.objects.create(
            device_id="1",
            latitude=34.0522,
            longitude=-118.2437,
            speed=50.0,
            timestamp="2024-11-19T12:00:00Z",
        )
        self.url = reverse("device-data")  # Your POST endpoint URL

    @patch("location.tasks.process_device_data.delay")
    def test_post_trigger_celery_task(self, mock_task):
        data = {
            "device_id": "1",
            "latitude": 34.0522,
            "longitude": -118.2437,
            "speed": 50.0,
            "timestamp": "2024-11-19T12:05:00Z",
        }

        response = self.client.post(self.url, data, format="json")

        # Assert that the Celery task was called
        mock_task.assert_called_once()

        # Assert that the response status code is 202 Accepted (accepted for processing)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        # Optionally, check the response data if needed
        self.assertEqual(response.data, {"message": "Data processing started."})
