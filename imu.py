import mpu6050
import time
import json
import paho.mqtt.client as mqtt

def setup_imu(broker_address="192.168.0.143", topic="sensors/imu"):
    mpu6050_sensor = mpu6050.mpu6050(0x68)
    
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
        
        print("Publishing: ", payload)
        client.publish(topic, json.dumps(payload))
        
        time.sleep(interval)

# Example of direct execution (optional)
if __name__ == "__main__":
    mpu, client, topic = setup_imu()
    publish_imu_data(mpu, client, topic)
