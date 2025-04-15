from gpiozero import PWMOutputDevice, DigitalOutputDevice
from time import sleep

# Pines conectados a la Raspberry Pi
PWM = PWMOutputDevice(17)      
IN1 = DigitalOutputDevice(27) 
IN2 = DigitalOutputDevice(22)  
#Oruga izquierda
PWM2 = PWMOutputDevice(12)
IN2_1 = DigitalOutputDevice(21)
IN2_2 = DigitalOutputDevice(11)
#Oruga derecha
PWM3 = PWMOutputDevice(13)
IN3_1 = DigitalOutputDevice(5)
IN3_2 = DigitalOutputDevice(6)
# Axis 1 (Rotación)
PWM5 = PWMOutputDevice(23)
PWM5_IN3_2 = DigitalOutputDevice(24)
PWM5_IN4_2 = DigitalOutputDevice(25)
# Axis 4 (Pala)
PWM6 = PWMOutputDevice(4)
PWM6_IN1_3 = DigitalOutputDevice(19)
PWM6_IN2_3 = DigitalOutputDevice(26)
# Axis 3 (Brazo superior)
PWM7 = PWMOutputDevice(15)
PWM7_IN3_3 = DigitalOutputDevice(16)
PWM7_IN4_3 = DigitalOutputDevice(20)

generalSpeed = 0.2

def move_axis1_Up():
    IN1.on()
    IN2.off()
    PWM.value = generalSpeed
def move_axis1_Down():
    IN1.off()
    IN2.on()
    PWM.value = generalSpeed
def Stop():
    PWM.off()
    IN1.off()
    IN2.off()
    IN2_1.off()
    IN2_2.off()
    IN3_1.off()
    IN3_2.off()
    PWM5_IN3_2.off()
    PWM5_IN4_2.off()
    PWM6_IN1_3.off() 
    PWM6_IN2_3.off()
    PWM7_IN3_3.off()
    PWM7_IN4_3.off()


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

def rotate_right():
   PWM5_IN3_2.on()
   PWM5_IN4_2.off()
   PWM5.value = generalSpeed
   
def rotate_left():
   PWM5_IN3_2.off()
   PWM5_IN4_2.on()
   PWM5.value = generalSpeed

def move_bucket_up():
    PWM6_IN1_3.on()
    PWM6_IN2_3.off()
    PWM6.value = generalSpeed

def move_bucket_down():
    PWM6_IN1_3.off()
    PWM6_IN2_3.on()
    PWM6.value = generalSpeed

def move_axis2_up():
    PWM7_IN3_3.on()
    PWM7_IN4_3.off()
    PWM7.value = generalSpeed

def move_axis2_down():
    PWM7_IN3_3.off()
    PWM7_IN4_3.on()
    PWM7.value = generalSpeed
# try:
#       while True:
#         opcion = input("Ingresa dirección (1=arriba, 2=abajo, 3=adelante, 5=rotacion, 4=atras, 6=pala upm 7=pala down, arm2 up =8, arm2 down = 9 0=detener,): ")

#         if opcion == "1":
#             PWM.value = 0.2
#             Up()
#         elif opcion == "2":
#             PWM.value = 0.2
#             Down()
#         elif opcion == "0":
#             Stop()
#             stop_movement()
#         elif opcion == "3":
#             PWM2.value = 0.2
#             right()
#             left()
#         elif opcion == "4":
#             PWM3.value = 0.2
#             back()
#         elif opcion == "6":
#             move_pala_up()
#         elif opcion == "7":
#             move_pala_down()
#         elif opcion == "8":
#             move_brazo_forward()
#         elif opcion == "9":
#             move_brazo_backward()
#         elif opcion == "5":
#             rotate_right()
#         elif opcion == "a":
#             rotate_left()
#         else:
#             print("1, 2 o 0.")
#         sleep(0.1)
# except KeyboardInterrupt:
#     print("Apagando motores...")
#     for p in [PWM, PWM2, PWM3]:
#         p.off()
#     for pin in [IN1, IN2, IN2_1, IN2_2, IN3_1, IN3_2]:
#         pin.off()
