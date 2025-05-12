import bulldozer
#import excavator

def get_command(payload):
    R_pedal = payload.get("right_pedal")
    L_pedal = payload.get("left_pedal")
    direction = payload.get("direction")
    arm = payload.get("arm_direction")
    arm_axis_1 = payload.get("arm_axis_1")
    arm_axis_2 = payload.get("arm_axis_2")
    arm_bucket = payload.get("arm_axis_3")
    rotation = payload.get("rotation")
    vehicle = payload.get("vehicle")
    if(vehicle == "bulldozer"):
           bulldozer_command(R_pedal,L_pedal,direction,arm)
    else:
           excavator_command(arm_axis_1,arm_axis_2,arm_bucket,direction,rotation, R_pedal,L_pedal)

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
                bulldozer.Down()
        case "down":
                bulldozer.Up()
        case "stop":
                bulldozer.Stop()
        case _:
                print("Invalid arm direction.........")
    
def excavator_command(arm_axis_1,arm_axis_2,arm_bucket,direction,rotation, R_pedal,L_pedal):
    if(R_pedal < 0 ):
            
            excavator.right(direction,R_pedal)
    else:
            excavator.stop_rigth()
    if(L_pedal < 0):
            excavator.left(direction,L_pedal)
    else:
            excavator.stop_left()     
    match arm_axis_1:
        case "up":
                excavator.move_axis1_Up()
        case "down":
                excavator.move_axis1_Down()
        case "stop":
                excavator.Stop()
    match arm_axis_2:
        case "up":
                excavator.move_axis2_up()
        case "down":
                excavator.move_axis2_down()
        case "stop":
                excavator.Stop()
    match arm_bucket:
        case "up":
                excavator.move_bucket_up()
        case "down":
                excavator.move_bucket_down()
        case "stop":
                excavator.Stop()
    match rotation:
        case "left":
                excavator.left(direction,rotation)
        case "right":
                excavator.right(direction,rotation)
        case "stop":
                excavator.stop_movement()
        case _:
            print("Invalid arm direction.........")
