import asyncio
import json
import django
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "locationous.settings")
django.setup()

from location.serializers.DeviceDataInput import DeviceDataInputSerializer
from location.tasks import process_device_data


class EchoTCPServer:
    def __init__(self, host="127.0.0.1", port=8888):
        self.host = host
        self.port = port

    async def handle_client(self, reader, writer):
        data = await reader.read(200)
        message = data.decode()
        addr = writer.get_extra_info("peername")
        print(f"Received '{message}' from {addr}")
        try:
            json_message = json.loads(message)
        except json.JSONDecodeError as e:
            writer.write("Invalid JSON data received: ".encode() + str(e).encode())
            writer.close()
            await writer.wait_closed()
            return
        serializer = DeviceDataInputSerializer(data=json_message)
        if not serializer.is_valid():
            print(f"Invalid data received: {message}")
            writer.write(("Invalid data received: " + str(serializer.errors)).encode())
        else:
            print(f"Valid data received: {serializer.validated_data}")
            # If validation passes, proceed with processing
            device_data = serializer.validated_data
            # Call the Celery task here
            process_device_data.delay(device_data)
            # Echo the message back to the client
            writer.write("Processing started.".encode())

        # Echo the message back to the client
        writer.write(data)
        await writer.drain()
        print("Sent message back to the client.")
        print()
        writer.close()
        await writer.wait_closed()

    async def start_server(self):
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        addr = server.sockets[0].getsockname()
        print(f"Serving on {addr}")
        async with server:
            await server.serve_forever()


# Run the TCP server as an asyncio task
tcp_server = EchoTCPServer()
loop = asyncio.get_event_loop()
loop.create_task(tcp_server.start_server())

# Run the Django ASGI application to handle HTTP requests if needed
application = get_asgi_application()

# This will allow you to run both Django and the custom TCP server asynchronously
loop.run_forever()
