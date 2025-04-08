import mpu6050
import time
import json
import paho.mqtt.client as mqtt
import socket

def get_local_ip():
    """Get the local IP address of the device."""
    try:
        # Create a socket to a common external server
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # We don't actually need to send data
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        print(f"Error determining local IP: {e}")
        return "localhost"

def setup_imu(broker_address=None, topic="raspberry/imu"):
    mpu6050_sensor = mpu6050.mpu6050(0x68)
    
    # Use the local IP if no broker address is provided
    if broker_address is None:
        broker_address = get_local_ip()
    
    client = mqtt.Client(protocol=mqtt.MQTTv5)
    client.connect(broker_address)
    
    return mpu6050_sensor, client, topic

def read_sensor_data(mpu):
    accelerometer_data = mpu.get_accel_data()
    gyroscope_data = mpu.get_gyro_data()
    
    return accelerometer_data, gyroscope_data

def publish_imu_data(mpu, client, topic, interval=1):
    while True:
        accel, gyro = read_sensor_data(mpu)
        
        payload = {
            "accelerometer": accel,
            "gyroscope": gyro
        }
        
        client.publish(topic, json.dumps(payload))
        
        time.sleep(interval)

# Example of direct execution (optional)
if __name__ == "__main__":
    mpu, client, topic = setup_imu()
    publish_imu_data(mpu, client, topic)
