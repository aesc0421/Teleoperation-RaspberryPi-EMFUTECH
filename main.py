import asyncio
import threading
import commands_mqtt_client
import web_rtc_server
import socket
import signal
from aiohttp import web
import imu
import ping_server
#import model1

def get_ip_address():
    try:
        # Create a socket to determine the output interface
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # We don't actually need to connect
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        # Fallback to localhost if we can't determine the IP
        return "127.0.0.1"

# Function to run the MQTT client in a separate thread
def run_mqtt_client():
    print("Starting MQTT client...")
    mqtt_client = commands_mqtt_client.create_mqtt_client()
    commands_mqtt_client.start_mqtt_loop(mqtt_client)

# Function to run the IMU sensor in a separate thread
def run_imu_sensor():
    print("Starting IMU sensor...")
    mpu, client, topic = imu.setup_imu()
    
    imu.publish_imu_data(mpu, client, topic)

# def run_motors():
#     print("Starting motors...")
#     run_mqtt_clien()

# Asynchronous function to run the WebRTC server
async def start_webrtc_server(stop_event: asyncio.Event):
    ip_address = get_ip_address()
    port = 8080
    
    print("Starting WebRTC server...")
    app = web_rtc_server.create_webrtc_app()
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Use 0.0.0.0 to listen on all network interfaces
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"WebRTC server started at http://{ip_address}:{port}")
    
    try:
        await stop_event.wait()
    finally:
        print("Stopping WebRTC server...")
        await runner.cleanup()

def create_shutdown_handler(stop_event: asyncio.Event):
    def handler():
        print("Shutdown signal received. Stopping services...")
        stop_event.set()
    return handler

async def main():
    ip_address = get_ip_address()
    print(f"Device IP: {ip_address}")

    stop_event = asyncio.Event()

    # Register the shutdown handler for system signals
    loop = asyncio.get_running_loop()
    shutdown_handler = create_shutdown_handler(stop_event)
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, shutdown_handler)

    mqtt_thread = threading.Thread(target=run_mqtt_client, daemon=True)
    mqtt_thread.start()
    
    # Start IMU sensor in a separate thread
    imu_thread = threading.Thread(target=run_imu_sensor, daemon=True)
    imu_thread.start()
    flask_thread = threading.Thread(target=ping_server.run_flask_server, daemon=True)
    flask_thread.start()
    await start_webrtc_server(stop_event)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("All services have been stopped correctly.")