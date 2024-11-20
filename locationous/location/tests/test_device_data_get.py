from django.test import tag
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from location.models import DeviceData


@tag("integration-test")
class DeviceDataGetAPITestCase(APITestCase):

    def setUp(self):
        # Set up some sample data for testing
        self.device_data1 = DeviceData.objects.create(
            device_id=1,
            latitude=34.0522,
            longitude=-118.2437,
            speed=50.0,
            timestamp="2024-11-19T12:00:00Z",
        )
        self.device_data2 = DeviceData.objects.create(
            device_id=1,
            latitude=34.0523,
            longitude=-118.2436,
            speed=55.0,
            timestamp="2024-11-19T12:05:00Z",
        )
        self.device_data3 = DeviceData.objects.create(
            device_id=2,
            latitude=40.7128,
            longitude=-74.0060,
            speed=60.0,
            timestamp="2024-11-19T12:10:00Z",
        )
        self.url = reverse("device-data")  # Your GET endpoint URL
        self.latest_url = reverse(
            "device-data-latest"
        )  # Your GET endpoint URL for latest data

    def test_get_device_data_latest(self):
        response = self.client.get(self.latest_url + "?device_id=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if only the latest device data entry is returned
        self.assertEqual(response.data["device_id"], "1")
        self.assertEqual(response.data["latitude"], 34.0523)
        self.assertEqual(response.data["longitude"], -118.2436)

    def test_get_device_data_with_date_range(self):
        response = self.client.get(
            self.url + "?start_date=2024-11-19T12:00:00Z&end_date=2024-11-19T12:05:00Z"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response includes only data within the specified range
        self.assertEqual(
            len(response.data), 2
        )  # Device ID 1 should have two entries within this range
