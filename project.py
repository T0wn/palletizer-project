
from robolink import *
from robodk import *
import CustomBox
import math
import time

sim = Robolink()

lab2Box = CustomBox.CustomBox("WoodBox", 48, 48, 48)
eirikBox = CustomBox.CustomBox("CustomBox", 80, 40, 50)
boxToUse = eirikBox

robot = sim.Item("UR10")
tool = sim.Item("CostumTool")
box = sim.Item(boxToUse.name)

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


box_length = boxToUse.length
box_width = boxToUse.width
box_heigth = boxToUse.height
boxes_per_layer = 9
boxes_per_pallet = 27
space_between_boxes = 10
speilvendt_stabling = False
pallet_length = 500
pallet_width = 300
target = leftTarget


def copy_new_box():
    box.Copy()
    new_box = sim.Paste(robotFrame)
    new_box.setPose(pickTarget * transl(0, 0, -box_heigth))

def pick_new_box():
    robot.MoveJ( pickTarget * transl(box_width / 2, box_length / 2, -100) )
    robot.MoveL( pickTarget * transl(box_width / 2, box_length / 2, -box_heigth) )
    tool.AttachClosest()
    robot.MoveL( pickTarget * transl(box_width / 2, box_length / 2, -100) )

# fix indent later
def place_box(x_pos, y_pos, z_pos):
    y_indent = 0
    x_indent = 0
    robot.MoveJ( target * transl(x_pos + x_indent, y_pos + y_indent, z_pos - 300) )
    robot.MoveL( target * transl(x_pos + x_indent, y_pos + y_indent, z_pos - 100) )
    robot.MoveL( target * transl(x_pos, y_pos, z_pos - box_heigth) )
    tool.DetachAll()
    robot.MoveL( target * transl(x_pos, y_pos, z_pos - 100) )

def get_pos_of_box(x, y, z):
    print(robotFrame.Pose() * target)

    # if ( (robotFrame.Pose() * target)[0][3] < 0 ):

# ikke complete
def box_per_direction():
    x = 3
    y = 3
    z = math.ceil( boxes_per_pallet / boxes_per_layer )
    return [x, y, z]

def palletize():
    stablemoonster = box_per_direction()
    x_max = stablemoonster[0]
    y_max = stablemoonster[1]
    z_max = stablemoonster[2]

    for y in range(0, y_max):

        y_pos = (box_length / 2) + y * (box_length + space_between_boxes)

        for x in range(0, x_max):

            x_pos = (box_width / 2) + x * (box_width + space_between_boxes)

            copy_new_box()
            pick_new_box()
            place_box(x_pos, y_pos, 0)

        


#programmet kjører herfra
if __name__ == "__main__":
    time.sleep(3)
    palletize()
    # copy_new_box()
    # pick_new_box()
    # place_box(0, 0, 0)