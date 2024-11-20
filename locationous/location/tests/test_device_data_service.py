from datetime import datetime
from unittest.mock import patch
from django.test import TestCase, tag
from location.models import DeviceData
from location.services import (
    get_latest_device_data,
    get_device_data_in_date_range,
    create_device_data,
)


@tag("unit-test")
class DeviceDataTests(TestCase):
    @patch("location.services.DeviceData.objects.create")
    def test_create_device_data(self, mock_create):
        # Data to be used in the creation function
        data = {
            "device_id": "device1",
            "timestamp": datetime(2024, 11, 20, 12, 0, 0),
            "latitude": 37.7749,
            "longitude": -122.4194,
            "speed": 50,
        }

        # Call the function
        create_device_data(data)

        # Check that the create method was called with the correct arguments
        mock_create.assert_called_once_with(
            device_id="device1",
            timestamp=datetime(2024, 11, 20, 12, 0, 0),
            latitude=37.7749,
            longitude=-122.4194,
            speed=50,
        )

    @patch("location.services.DeviceData.objects.filter")
    def test_get_latest_device_data(self, mock_filter):
        # Mock the response of the filter query
        mock_filter.return_value.order_by.return_value.first.return_value = DeviceData(
            device_id="device1", timestamp=datetime(2024, 11, 20, 12, 0, 0)
        )

        # Call the function
        result = get_latest_device_data("device1")

        # Check that the mock filter method was called with the correct arguments
        mock_filter.assert_called_once_with(device_id="device1")
        mock_filter.return_value.order_by.assert_called_once_with("-timestamp")
        self.assertEqual(result.device_id, "device1")
        self.assertEqual(result.timestamp, datetime(2024, 11, 20, 12, 0, 0))

    @patch("location.services.DeviceData.objects.filter")
    def test_get_device_data_in_date_range(self, mock_filter):
        # Mock the return value of the filter query
        mock_filter.return_value.order_by.return_value.values.return_value = [
            {
                "device_id": "device1",
                "timestamp": "2024-11-20 12:00:00",
                "latitude": 37.7749,
                "longitude": -122.4194,
                "speed": 50,
            }
        ]

        # Mock dates for the range
        start_date = datetime(2024, 11, 20, 0, 0, 0)
        end_date = datetime(2024, 11, 20, 23, 59, 59)

        # Call the function
        result = get_device_data_in_date_range(start_date, end_date)

        # Check that the filter method was called with the correct date range
        mock_filter.assert_called_once_with(timestamp__range=[start_date, end_date])
        mock_filter.return_value.order_by.assert_called_once_with("-timestamp")
        mock_filter.return_value.order_by.return_value.values.assert_called_once()

        # Verify the returned data
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["device_id"], "device1")
        self.assertEqual(result[0]["latitude"], 37.7749)
        self.assertEqual(result[0]["longitude"], -122.4194)
        self.assertEqual(result[0]["speed"], 50)
