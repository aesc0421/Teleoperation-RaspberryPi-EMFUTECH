from gpiozero import PWMOutputDevice, DigitalOutputDevice
from time import sleep

# Pines conectados a la Raspberry Pi
PWM = PWMOutputDevice(17)      # ENA del L298N - velocidad
IN1 = DigitalOutputDevice(27)  # IN1 del L298N - dirección
IN2 = DigitalOutputDevice(22)  # IN2 del L298N - dirección
#Oruga izquierda
PWM2 = PWMOutputDevice(12)
IN2_1 = DigitalOutputDevice(23)
IN2_2 = DigitalOutputDevice(24)

#Oruga derecha
PWM3 = PWMOutputDevice(13)
IN3_1 = DigitalOutputDevice(5)
IN3_2 = DigitalOutputDevice(6)


#Axis 2 Brazo inferior
PWM4 = PWMOutputDevice(17)
PWM4_IN1_2 = DigitalOutputDevice(27)
PWM4_IN2_2 = DigitalOutputDevice(2)

# Axis 1 (Rotación)
PWM5 = PWMOutputDevice(23)
PWM5_IN3_2 = DigitalOutputDevice(24)
PWM5_IN4_2 = DigitalOutputDevice(25)

# Axis 4 (Pala)
PWM6 = PWMOutputDevice(14)
PWM6_IN1_3 = DigitalOutputDevice(19)
PWM6_IN2_3 = DigitalOutputDevice(26)

# Axis 3 (Brazo superior)
PWM7 = PWMOutputDevice(15)
PWM7_IN3_3 = DigitalOutputDevice(16)
PWM7_IN4_3 = DigitalOutputDevice(20)



def Up():
    IN1.on()
    IN2.off()
    PWM.value = 0.5
   

def Down():
    IN1.off()
    IN2.on()
    PWM.value = 0.5


def Stop():
    PWM.value = 0.1
    PWM.off()
    IN1.off()
    IN2.off()


def back(value):
    IN2_1.on()
    IN2_2.off()
    IN3_1.on()
    IN3_2.off()
    value = abs(value)
    PWM2.value = value
    PWM3.value = value

def forward(value):
    IN2_1.off()
    IN2_2.on()
    IN3_1.off()
    IN3_2.on()
    value = abs(value)
    PWM2.value = value
    PWM3.value = value

def stop_movement():
    PWM2.off()
    PWM3.off()
    IN2_1.off()
    IN2_2.off()
    IN3_1.off()
    IN3_2.off()

def stop_rigth():
    PWM3.off()
def stop_left():
    PWM2.off()

def right(direction, value):
    value = abs(value)
    if direction == "forward":
        IN3_1.off()
        IN3_2.on()
    elif direction == "backward":
        IN3_1.on()
        IN3_2.off()
    else:
        IN3_1.off()
        IN3_2.off()
        value = 0
    PWM3.value = value

def left(direction, value):
    value = abs(value)
    if direction == "forward":
        IN2_1.off()
        IN2_2.on()
    elif direction == "backward":
        IN2_1.on()
        IN2_2.off()
    else:
        IN2_1.off()
        IN2_2.off()
        value = 0
    PWM2.value = value