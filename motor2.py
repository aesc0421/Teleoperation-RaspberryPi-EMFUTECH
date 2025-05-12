from gpiozero import PWMOutputDevice, DigitalOutputDevice
from time import sleep

# Pines conectados a la Raspberry Pi
PWM = PWMOutputDevice(17)      # ENA del L298N - velocidad
IN1 = DigitalOutputDevice(27)  # IN1 del L298N - dirección
IN2 = DigitalOutputDevice(22)  # IN2 del L298N - dirección

def forward(velocity:int):
    IN1.on()
    IN2.off()
    PWM.value = velocity
   

def backward(velocity:int):
    IN1.off()
    IN2.on()
    PWM.value = velocity


def stop():
    PWM.value = 0.2
    PWM.off()
    IN1.off()
    IN2.off()


try:
      while True:
        opcion = input("Ingresa dirección (1=adelante, 2=atrás, 0=detener): ")

        if opcion == "1":
            PWM.value = 0.2
            forward()
        elif opcion == "2":
            PWM.value = 0.2
            backward()
        elif opcion == "0":
            stop()
        else:
            print("1, 2 o 0.")
        
        sleep(0.1)
except KeyboardInterrupt:
    print("\n⛔ Interrumpido por el usuario. Apagando motor.")
    PWM.off()
    IN1.off()
    IN2.off()



