
from robolink import *
from robodk import *
import CustomBox
import math

sim = Robolink()

#boxes
# lab2Box = CustomBox.CustomBox("WoodBox", 48, 48, 48)
# box1 = CustomBox.CustomBox("Box1", 80, 40, 50)
box2 = CustomBox.CustomBox("Box2", 100, 80, 50)
# boxToUse = box2

robot = sim.Item("UR10")
tool = sim.Item("CostumTool")

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

target = rightTarget


def copy_new_box(box, box_height):
    box.Copy()
    new_box = sim.Paste(robotFrame)
    new_box.setPose(pickTarget * transl(0, 0, -box_height))

def pick_new_box(box_length, box_width, box_height):
    robot.MoveJ( pickTarget * transl(box_width / 2, box_length / 2, -100) )
    robot.MoveL( pickTarget * transl(box_width / 2, box_length / 2, -box_height) )
    tool.AttachClosest()
    robot.MoveL( pickTarget * transl(box_width / 2, box_length / 2, -100) )

# fix indent later
def place_box(x_pos, y_pos, z_pos, box_height, space_between_boxes):
    y_indent = getIndent(space_between_boxes)
    x_indent = 0
    robot.MoveJ( target * transl(x_pos + x_indent, y_pos + y_indent, z_pos - 300) )
    robot.MoveL( target * transl(x_pos + x_indent, y_pos + y_indent, z_pos - 100) )
    robot.MoveL( target * transl(x_pos, y_pos, z_pos - box_height) )
    tool.DetachAll()
    robot.MoveL( target * transl(x_pos, y_pos, z_pos - 100) )

def getIndent(space_between_boxes):
    nr = 10
    if (space_between_boxes < 10):
        nr = 100

    if ( robodk.Pose_2_ABB(pickTarget * target)[1] < 0 ):
        return nr
    else:
        return -nr

def get_pos_of_box(x, y, z, x_max, y_max, box_length, box_width, box_height, space_between_boxes):
    if ( robodk.Pose_2_ABB(pickTarget * target)[1] < 0 ):
        y_pos = (box_length / 2) + y * (box_length + space_between_boxes)
    else:
        y_pos = (box_length / 2) + ( (y_max - 1) * (box_length + space_between_boxes) ) - ( y * (box_length + space_between_boxes) )

    x_pos = (box_width / 2) + x * (box_width + space_between_boxes)
    z_pos = -box_height * z

    return [x_pos, y_pos, z_pos]


# ikke complete
def box_per_direction():
    x = 3
    y = 3
    z = math.ceil( boxes_per_pallet / boxes_per_layer )
    return [x, y, z]

def calcheight(boxes_per_pallet, x, y):
    return math.ceil( boxes_per_pallet / (x * y) )

def palletize(box_object, boxes_in_z_dir, boxes_in_x_dir, boxes_in_y_dir, space_between_boxes):
    box = sim.Item(box_object.name)
    box_length = box_object.length
    box_width = box_object.width
    box_height = box_object.height

    # stablemoonster = box_per_direction()
    x_max = boxes_in_x_dir
    y_max = boxes_in_y_dir
    z_max = boxes_in_z_dir

    for z in range(0, z_max):
        for y in range(0, y_max):
            for x in range(0, x_max):

                positions = get_pos_of_box(x, y, z, x_max, y_max, box_length, box_width, box_height, space_between_boxes)
                x_pos = positions[0]
                y_pos = positions[1]
                z_pos = positions[2]

                copy_new_box(box, box_height)
                pick_new_box(box_length, box_width, box_height)
                place_box(x_pos, y_pos, z_pos, box_height, space_between_boxes)

    


#programmet kjører herfra
if __name__ == "__main__":
    palletize(box2, 3, 3, 3, 10)