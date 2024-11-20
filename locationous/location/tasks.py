from celery import shared_task

from location.services import create_device_data


@shared_task
def process_device_data(data):
    # Process and save data to the database
    create_device_data(data)
