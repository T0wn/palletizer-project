
from robolink import *
from robodk import *
import math
import time

sim = Robolink()

robot = sim.Item("UR10")
tool = sim.Item("CostumTool")
box = sim.Item("WoodBox")

robotFrame = sim.Item('UR10 Base')

#frames
pickFrame = sim.Item("pickFrame")
leftFrame = sim.Item("placeFrameLeft")
rightFrame = sim.Item("placeFrameRight")

#targets
home = sim.Item("Home")
pickTarget = Mat(pickFrame.Pose() * roty(pi) * rotz(pi/2))
leftTarget = Mat(pickFrame.Pose() * leftFrame.Pose() * roty(pi) * rotz(pi/2))
rightTarget = Mat(pickFrame.Pose() * rightFrame.Pose() * roty(pi) * rotz(pi/2))


box_length = 48
box_width = 48
box_heigth = 48
boxes_per_layer = 9
boxes_per_pallet = 27
space_between_boxes = 10
speilvendt_stabling = False
pallet_length = 500
pallet_width = 300


def copy_new_box():
    box.Copy()
    new_box = sim.Paste(robotFrame)
    new_box.setPose(pickTarget * rotx(-pi/2))

def pick_new_box():
    robot.MoveJ( pickTarget * transl(box_length / 2, box_width / 2, -100) )
    robot.MoveL( pickTarget * transl(box_length / 2, box_width / 2, -box_heigth) )
    tool.AttachClosest()
    robot.MoveL( pickTarget * transl(box_length / 2, box_width / 2, -100) )

def place_box(target, x_pos, y_pos, z_pos):
    print(robotFrame.Pose() * target)

    y_indent = 0
    # if ( (robotFrame.Pose() * target)[0][3] < 0 ):
        

    robot.MoveJ( target * transl(x_pos, y_pos + y_indent, z_pos - 300) )
    robot.MoveL( target * transl(x_pos, y_pos + y_indent, z_pos - 100) )
    robot.MoveL( target * transl(x_pos, y_pos, z_pos - box_heigth) )
    tool.DetachAll()
    robot.MoveL( target * transl(x_pos, y_pos, z_pos - 100) )

# ikke complete
def box_per_direction(boxes_per_pallet, boxes_per_layer, pallet_length, pallet_width):
    x = 3
    y = 3
    z = math.ceil( boxes_per_pallet / boxes_per_layer )
    return [x, y, z]

def palletize(box_length, box_width, box_heigth, space_between_boxes, boxes_per_layer, speilvendt_stabling, pallet_length, pallet_width):
    stablemoonster = box_per_direction(boxes_per_pallet, boxes_per_layer, pallet_length, pallet_width)
    for y in range (0, stablemoonster[2]):

        y_pos = (box_width / 2) + y * (box_width + space_between_boxes)

        copy_new_box()
        pick_new_box()

        



#programmet kjører herfra
if __name__ == "__main__":
    time.sleep(3)
    # palletize(box_length, box_width, box_heigth, space_between_boxes, boxes_per_layer, speilvendt_stabling, pallet_length, pallet_width)
    copy_new_box()
    pick_new_box()
    place_box(leftTarget, 0, 0, 0)