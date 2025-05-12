import bulldozer
import time
import imu
from current_orientation import current_position


def get_gyro_z():
    accel, gyro = imu.get_imu_data()
   # print(gyro)
    return gyro['z']    


def rotate_right_90(speed=1):
    target_angle = 90  # grados
    angle_accum = 0
    last_time = time.perf_counter()

    bulldozer.right("forward", speed)
    bulldozer.left("backward", speed /2) 
    
    while abs(angle_accum) < target_angle:
        current_time = time.perf_counter()
        dt = current_time - last_time
        last_time = current_time

        gyro_z = get_gyro_z()  # en grados/segundo
        angle_accum += gyro_z * dt  # integración: Δθ = ω * Δt
        time.sleep(0.01)

    bulldozer.stop_movement()
    time.sleep(0.5)

def rotate_left_90(speed=1):
    target_angle = 90  # grados
    angle_accum = 0
    last_time = time.perf_counter()

    bulldozer.right("backward", speed/2)
    bulldozer.left("forward", speed ) 
    
    while abs(angle_accum) < target_angle:
        current_time = time.perf_counter()
        dt = current_time - last_time
        last_time = current_time
        gyro_z = get_gyro_z()  
        angle_accum += gyro_z * dt  #Δθ = ω * Δt
        time.sleep(0.01)

    bulldozer.stop_movement()
    time.sleep(0.5)
    

def rotate_180(speed=0.85):
    target_angle = 180  # grados
    angle_accum = 0
    last_time = time.perf_counter()

    bulldozer.right("backward", speed)
    bulldozer.left("forward", speed) 
    
    while abs(angle_accum) < target_angle:
        current_time = time.perf_counter()
        dt = current_time - last_time
        last_time = current_time

        gyro_z = get_gyro_z()  # en grados/segundo
        angle_accum += gyro_z * dt  # integración: Δθ = ω * Δt
        time.sleep(0.01)
    bulldozer.stop_movement()
    time.sleep(0.5)

    

def follow_oriented_path(instructions):
    for step in instructions:
        parsed = step.split()  # ['forward', '3']
        action = parsed[0]        # 'forward'
        value = (parsed[1]) 
        if action == "forward":
            print("forwardo")
            bulldozer.left("forward",0.4)
            bulldozer.right("forward",0.4)
            for i in range(0,int(value)):
                maintain_heading_forward(0.5,0.4,2)
                time.sleep(1.5)
        elif action == "turn":
            if value == "right":
                print("left")
                rotate_left_90()
            elif value == "left":
                print("rigth")
                rotate_right_90()
            elif value == "around":
                rotate_180()

def maintain_heading_forward(duration, speed, tolerance=2):
    yaw_ref = get_gyro_z()  
    start_time = time.perf_counter()

    while time.perf_counter() - start_time < duration:
        current_yaw = get_gyro_z()
        error = current_yaw - yaw_ref

       
        if error > 180:
            error -= 360
        elif error < -180:
            error += 360

        if abs(error) < tolerance:

            print("recto")
            bulldozer.right("forward",speed)
            bulldozer.left("forward",speed)
        elif error > 0:
            print("corrección 1")
            # se está desviando a la izquierda → corrige hacia la derecha
            bulldozer.right("forward",speed - 0.1)
            bulldozer.left("forward",speed + 0.1)
        else:
            print("corrección 2")
            # se está desviando a la derecha → corrige hacia la izquierda
            bulldozer.right("forward",speed + 0.1)
            bulldozer.left("forward",speed - 0.1)

        time.sleep(0.05)

    bulldozer.stop_movement()


def path_to_instructions(path):
    global current_position
    DIRECTIONS = {
        (-1, 0): "up",
        (0, 1): "right",
        (1, 0): "down",
        (0, -1): "left"
    }

    DIR_ORDER = ["up", "right", "down", "left"]

    if len(path) < 2:
        return []

    instructions = []
    orientation = current_position
    count = 0

    for i in range(1, len(path)):
        prev = path[i - 1]
        curr = path[i]
        delta = (curr[0] - prev[0], curr[1] - prev[1])
        if delta not in DIRECTIONS:
            print(f"{prev} -> {curr}")
            continue
        direction = DIRECTIONS[delta]
        print("current direction", direction)

        if direction == orientation:
            count += 1
        else:
            if count > 0:
                instructions.append(f"forward {count}")
                count = 0
            # hacer el giro
            current_idx = DIR_ORDER.index(orientation)
            target_idx = DIR_ORDER.index(direction)
            turn = (target_idx - current_idx) % 4
            if turn == 1:
                current_position = "left"
                instructions.append("turn right")
            elif turn == 3:
                current_position = "right"
                instructions.append("turn left")
            elif turn == 2:
                instructions.append("turn around")
                if current_position == "up":
                    current_position = "down"
                else:
                    current_position = "up"
            orientation = direction
            count = 1 

    if count > 0:
        instructions.append(f"forward {count}")
    print("final orientation", current_position)
    orientation = direction
    current_position = direction  
    return instructions

# new_path = [(6, 5), (5, 5), (4, 5), (3, 5), (2, 5), (1, 5), (0, 5), (0, 4), (0, 3),(0, 2), (0, 1), (1, 1), (2, 1),(3, 1), (4, 1), (5, 1), (6, 1),(7,1),(8,1)]

# path =     [(2, 4), (3, 4), (4, 4)]
# result = path_to_instructions(path, start_orientation="left")
# # print(result)
# # #maintain_heading_forward(1.3,0.3,2) ## recorre una hoja  
# follow_oriented_path(result)




