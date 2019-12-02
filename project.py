
from robolink import *
from robodk import *
import CustomBox
import datahandler as dh
import math

sim = Robolink()

robot = sim.Item("UR10")
tool = sim.Item("CostumTool")


#frames
robotFrame = sim.Item('UR10 Base')
pickFrame = sim.Item("pickFrame")
leftFrame = sim.Item("placeFrameLeft")
rightFrame = sim.Item("placeFrameRight")

#targets
home = sim.Item("Home")
pickTarget = Mat(pickFrame.Pose() * roty(pi) * rotz(pi/2))
leftTarget = Mat(pickFrame.Pose() * leftFrame.Pose() * roty(pi) * rotz(pi/2))
rightTarget = Mat(pickFrame.Pose() * rightFrame.Pose() * roty(pi) * rotz(pi/2))


def getTarget(targetnr):
    targets = [leftTarget, rightTarget]
    return targets[targetnr]


def copy_new_box(box, box_height):
    box.Copy()
    new_box = sim.Paste(robotFrame)
    new_box.setPose(pickTarget * transl(0, 0, -box_height))


def pick_new_box(box_length, box_width, box_height, layerHeight):
    robot.MoveJ( pickTarget * transl(box_width / 2, box_length / 2, -100) )
    robot.MoveL( pickTarget * transl(box_width / 2, box_length / 2, -box_height) )
    tool.AttachClosest()
    robot.MoveL( pickTarget * transl(box_width / 2, box_length / 2, -((box_height * (1 + layerHeight)) + 100)) )


def place_box(x_pos, y_pos, z_pos, box_height, space_between_boxes, target, patern):
    y_indent = getIndent(space_between_boxes, target)
    x_indent = 0
    
    # brukes hvis det ønskes custom plasering/rotasjon av boxer
    rotation, x_move, y_move = patern

    robot.MoveJ( target * transl(x_pos + x_indent, y_pos + y_indent, z_pos - box_height - 250) * rotz((rotation/180) * pi))
    robot.MoveL( target * transl(x_pos + x_indent, y_pos + y_indent, z_pos - box_height - 50) * rotz((rotation/180) * pi))
    robot.MoveL( target * transl(x_pos, y_pos, z_pos - box_height) * rotz((rotation/180) * pi))
    tool.DetachAll()
    robot.MoveL( target * transl(x_pos, y_pos, z_pos - box_height - 100) )  


def getIndent(space_between_boxes, target):
    indent = 10
    if (space_between_boxes < 10):
        indent = 100

    # setter fortegn på indent utfra hvilken side av roboten target er på
    if ( robodk.Pose_2_ABB(pickTarget * target)[1] < 0 ):
        return indent
    else:
        return -indent


def get_pos_of_box(x, y, z, x_move, y_move, y_max, box_length, box_width, box_height, space_between_boxes, target):
    if ( robodk.Pose_2_ABB(pickTarget * target)[1] < 0 ):
        y_pos = (box_length / 2) + y * (box_length + space_between_boxes) + x_move
    else:
        y_pos = (box_length / 2) + ( (y_max - 1) * (box_length + space_between_boxes) ) - ( y * (box_length + space_between_boxes) ) + x_move

    x_pos = (box_width / 2) + x * (box_width + space_between_boxes) + y_move
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


def palletize(box_object, targetnr, boxes_in_x_dir, boxes_in_y_dir, boxes_in_z_dir, space_between_boxes, layer_pattern = None):
    box = sim.Item(box_object.name)
    box_length = box_object.length
    box_width = box_object.width
    box_height = box_object.height
    target = getTarget(targetnr)

    # stablemoonster = box_per_direction()
    x_max = boxes_in_x_dir
    y_max = boxes_in_y_dir
    z_max = boxes_in_z_dir

    # genererer default pattern, hvis et custom pattern ikke er oppgitt
    if (layer_pattern == None):
        layer_pattern = []
        for y in range(0, y_max):
            layer_pattern.append([])
            for x in range(0, x_max):
                layer_pattern[y].append( (0, 0, 0) )

    for z in range(0, z_max):
        for y in range(0, y_max):
            for x in range(0, x_max):

                rotation = layer_pattern[y][x][0]
                x_move, y_move = layer_pattern[y][x][1:3]
                x_pos, y_pos, z_pos = get_pos_of_box(x, y, z, x_move, y_move, y_max, box_length, box_width, box_height, space_between_boxes, target)

                # sjekker om box skal plasseres eller ikke
                if (rotation >= 0):
                    copy_new_box(box, box_height)
                    pick_new_box(box_length, box_width, box_height, z)
                    place_box(x_pos, y_pos, z_pos, box_height, space_between_boxes, target, layer_pattern[y][x])

    robot.MoveJ(home)



# TODO les array andre veien utfra hvor den stabler.

# (rotation, x-forskyvning, y-forskyvning)
# rotation options: -1 = plasserer ikke box      x = roterer x grader
testArray = [
    [(90, -30, 15), (-1, 0, 0), (90, -30, -15)],
    [(0, 0, 0), (0, 0, 0), (0, 0, 0)],
    [(90, 30, 15), (-1, 0, 0), (90, 30, -15)]
]

if __name__ == "__main__":
    # palletize(dh.datahandler.getBoxes()[1], 1, 3, 3, 2, 20, layer_pattern = testArray)
    palletize( dh.datahandler.getBoxes()[2], 1, 4, 1, 3, 5)#, layer_pattern = testArray )