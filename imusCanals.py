import smbus2
import time
import mpu6050
import time
import json
import paho.mqtt.client as mqtt
import socket


# Direcciones
MULTIPLEXER_ADDR = 0x70
MPU_ADDR = 0x68
channels = [1, 2, 3]  # Canales del multiplexor con sensores conectados

# Registros MPU6050
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

bus = smbus2.SMBus(1)


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

def select_channel(channel):
    """Activa el canal del multiplexor TCA9548A."""
    bus.write_byte(MULTIPLEXER_ADDR, 1 << channel)
    time.sleep(0.01)

def init_mpu():
    """Despierta el MPU6050"""
    bus.write_byte_data(MPU_ADDR, PWR_MGMT_1, 0)

def read_word(reg):
    high = bus.read_byte_data(MPU_ADDR, reg)
    low = bus.read_byte_data(MPU_ADDR, reg + 1)
    value = (high << 8) + low
    if value >= 0x8000:
        value = -((65535 - value) + 1)
    return value

def read_imu():
    """Lee acelerómetro y giroscopio del MPU6050"""
    accel_x = read_word(ACCEL_XOUT_H)
    accel_y = read_word(ACCEL_XOUT_H + 2)
    accel_z = read_word(ACCEL_XOUT_H + 4)
    gyro_x = read_word(GYRO_XOUT_H)
    gyro_y = read_word(GYRO_XOUT_H + 2)
    gyro_z = read_word(GYRO_XOUT_H + 4)
    return {
        "accel": {"X":accel_x,"Y": accel_y,"Z":accel_z},
        "gyro": {"X":gyro_x,"Y": gyro_y,"Z": gyro_z}
    }


# Inicializa sensores
for ch in channels:
    select_channel(ch)
    try:
        init_mpu()
        print(f"Canal {ch} inicializado.")
    except Exception as e:
        print(f"Error inicializando canal {ch}: {e}")

print("\n--- Lecturas en tiempo real ---\n")
def send_data(sensor, accel,gyro):
    payload = {
        "sensor":sensor,
        "acc":accel,
        "gyro":gyro
    }
    return payload

def publish_imu_data(mpu, client, topic, interval=0.01):

    print("payload", mpu)
    client.publish(topic, json.dumps(mpu))
    
   # time.sleep(interval)



def publis_multiple_imu_sensors(client,topic,interval):
  while True:
    imu_data_list = []

    for ch in channels:
        try:
            select_channel(ch)
            data = read_imu()
            imu_data_list.append({
                "channel": ch,
                "accel": data['accel'],
                "gyro": data['gyro']
            })
        except Exception as e:
            print(f"Error en canal {ch}: {e}")
    
    publish_imu_data(
        mpu=imu_data_list,
        client=client,
        topic=topic,
        interval=interval
    )
    print("-" * 60)
    #time.sleep(0.01)