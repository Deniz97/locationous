from location.serializers.DeviceData import DeviceDataSerializer
from location.serializers.DeviceDataInput import DeviceDataInputSerializer
from location.models import DeviceData

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from location.models import DeviceData
from location.tasks import process_device_data
from location.services import (
    get_device_data_in_date_range,
    get_latest_device_data,
)


class DeviceDataAPI(APIView):
    def post(self, request, *args, **kwargs):
        """
        Endpoint to accept device data and trigger a Celery task.
        """
        # Parse the JSON payload
        serializer = DeviceDataInputSerializer(data=request.data)

        if serializer.is_valid():
            # If validation passes, proceed with processing
            device_data = serializer.validated_data
            # Call the Celery task here
            process_device_data.delay(device_data)
            return Response(
                {"message": "Data processing started."}, status=status.HTTP_202_ACCEPTED
            )

        # If validation fails, return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests for both:
        - /api/device-data/latest (for the latest data of a specific device)
        - /api/device-data (for data within a date range)
        """
        if kwargs.get("action") == "latest":
            # Handle the `/latest` endpoint
            device_id = request.query_params.get("device_id")
            if not device_id:
                return Response(
                    {"error": "Missing 'device_id' parameter"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            latest_data = get_latest_device_data(device_id)
            if not latest_data:
                return Response(
                    {"error": "No data found for the given device_id"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = DeviceDataSerializer(latest_data)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        # Handle the `/` endpoint (date range query)
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        if not start_date or not end_date:
            return Response(
                {"error": "Missing 'start_date' or 'end_date' parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        device_data = get_device_data_in_date_range(start_date, end_date)
        # Serialize the data
        serializer = DeviceDataSerializer(device_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
