import paho.mqtt.client as mqtt
import json
import socket
import command_parse_service
import excavator
# Get local IP address
def get_local_ip():
    try:
        # Create a socket that connects to an external server
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Doesn't actually send data
        s.connect(("8.8.8.8", 80))
        # Get the local IP address used for the connection
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        print(f"Error getting local IP: {e}")
        return "localhost"  # Fallback to localhost

# Called when the client connects to the broker
def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == mqtt.CONNACK_ACCEPTED:
        print("Connected to MQTT broker")
        client.subscribe("raspberry/controls")  # Subscribe to your control topic
    else:
        print("Failed to connect, return code:", reason_code)

# Called when a message is received from the broker
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print(f"{payload} Commands MQTT file ")
        command_parse_service.get_command(payload)
    except Exception as e:
        print("Error decoding message:", e)
        return None

def create_mqtt_client(broker_address=None, port=1883, keepalive=60):
    # Use the local IP if no broker address is provided
    if broker_address is None:
        broker_address = get_local_ip()
        print(f"Using local IP as broker address: {broker_address}")
    
    # Create the MQTT client
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    
    # Set up event handlers
    client.on_connect = on_connect
    client.on_message = on_message
    # todo send to motors functtion pene pene 
    print("message")
    
    # Connect to broker
    client.connect(broker_address, port, keepalive)
    return client

def start_mqtt_loop(client):
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("Disconnecting...")
        client.disconnect()
        print("Successfully disconnected.")

# To allow the script to be run directly or be imported as a module
if __name__ == "__main__":
    # This code will only run if you run this file directly
    mqtt_client = create_mqtt_client()
    start_mqtt_loop(mqtt_client)
