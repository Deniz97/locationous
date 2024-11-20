from location.models import DeviceData


def get_latest_device_data(device_id):
    return DeviceData.objects.filter(device_id=device_id).order_by("-timestamp").first()


def get_device_data_in_date_range(start_date, end_date):
    return (
        DeviceData.objects.filter(timestamp__range=[start_date, end_date])
        .order_by("-timestamp")
        .values()
    )


def create_device_data(data):
    DeviceData.objects.create(
        device_id=data["device_id"],
        timestamp=data["timestamp"],
        latitude=data["latitude"],
        longitude=data["longitude"],
        speed=data["speed"],
    )
