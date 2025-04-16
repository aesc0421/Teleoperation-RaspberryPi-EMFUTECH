import bulldozer
#import excavator

def get_command(payload):
    R_pedal = payload.get("right_pedal")
    L_pedal = payload.get("left_pedal")
    direction = payload.get("direction")
    arm = payload.get("arm_direction")
    vehicle = payload.get("vehicle")
    if(vehicle == "bulldozer"):
           bulldozer_command(R_pedal,L_pedal,direction,arm)
    else:
           excavator_command(R_pedal,L_pedal,direction,arm)

def bulldozer_command(R_pedal,L_pedal,direction,arm):
    if(R_pedal < 0 ):
            bulldozer.right(direction,R_pedal)
    else:
            bulldozer.stop_rigth()
    if(L_pedal < 0):
            bulldozer.left(direction,L_pedal)
    else:
            bulldozer.stop_left()     
    match arm:
        case "up":
                bulldozer.Up()
        case "down":
                bulldozer.Down()
        case "stop":
                bulldozer.Stop()
        case _:
                print("Invalid arm direction.........")
    
def excavator_command(R_pedal,L_pedal,direction,arm):
    if(R_pedal < 0 ):
            
            excavator.right(direction,R_pedal)
    else:
            excavator.stop_rigth()
    if(L_pedal < 0):
            excavator.left(direction,L_pedal)
    else:
            excavator.stop_left()     
    match arm:
        case "rotate_right":
            excavator.rotate_right()
        case "rotate_left":
            excavator.rotate_left()
        case "up_axis_1":
            excavator.move_axis1_Up()
        case "down_axis_1":
            excavator.move_axis1_Down()
        case "up_axis_2":
            excavator.move_axis2_up()
        case "down_axis_2":
            excavator.move_axis2_down()
        case "up_bucket":
            excavator.move_bucket_up()
        case "down_bucket":
            excavator.move_bucket_down()
        case "stop":
            excavator.Stop()
        case _:
            print("Invalid arm direction.........")