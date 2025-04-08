import paho.mqtt.client as mqtt
import json

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
        print(payload)
        # You can add additional logic here to handle different commands
        return payload
    except Exception as e:
        print("Error decoding message:", e)
        return None

def create_mqtt_client(broker_address="192.168.0.236", port=1884, keepalive=60):
    # Create the MQTT client
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    
    # Set up event handlers
    client.on_connect = on_connect
    client.on_message = on_message
    
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
