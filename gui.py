import tkinter as tk
import tkinter.ttk as ttk
import project
import CustomBox


# lager ny label og inputfield
def newInput(root, msg, pos1, pos2):
    lbl = tk.Label(root, text=msg)
    lbl.grid(column=pos1, row=pos2, padx=0, pady=2)
    inpt = tk.Entry(root, width=10)
    inpt.grid(column=pos1+1, row=pos2, padx=0, pady=2)
    return inpt

def palletizeClick():
    boxObject = getBoxes()[combo.current()]
    target = targetCombo.current()
    boxes_in_z_dir = int(inputArray[0].get())
    boxes_in_x_dir = int(inputArray[1].get())
    boxes_in_y_dir = int(inputArray[2].get())
    space_between_boxes = int(inputArray[3].get())

    project.palletize(boxObject, target, boxes_in_x_dir, boxes_in_y_dir, boxes_in_z_dir, space_between_boxes)

def addCustomBox():
    print("ikke implementert enda")

lab2Box = CustomBox.CustomBox("WoodBox", 48, 48, 48)
box1 = CustomBox.CustomBox("Box1", 80, 40, 50)
box2 = CustomBox.CustomBox("Box2", 100, 80, 50)

def getBoxes():
    boxes = [lab2Box, box1, box2]
    return boxes


root = tk.Tk()
root.title("UR10 Palletizing")

grid = tk.Grid()

inputArray = []
# inputArray.append( newInput(root, "Name of box to copy:", 1, 1) )
# inputArray.append( newInput(root, "Box length:", 1, 2) )
# inputArray.append( newInput(root, "Box width:", 1, 3) )
# inputArray.append( newInput(root, "Box heigth:", 1, 4) )

label = tk.Label(root, text="Choose box:").grid(column=1, row=2)
combo = ttk.Combobox(root, width=15)
combo['values'] = getBoxes()
combo.grid(column=2, row=2)

btn = tk.Button(root, text="Add a custom box", command=addCustomBox).grid(column=2, row=3)

targetLabel = tk.Label(root, text="Choose target:").grid(column=1, row=4)
targetCombo = ttk.Combobox(root, width=15)
targetCombo['values'] = ("Left target", "Rigth target")
targetCombo.grid(column=2, row=4)

inputArray.append( newInput(root, "Number of layers:", 1, 5) )
inputArray.append( newInput(root, "Boxes in x direction on layer:", 1, 6) )
inputArray.append( newInput(root, "Boxes in y direction on layer:", 1, 7) )
inputArray.append( newInput(root, "Space between boxes:", 1, 8) )

label2 = tk.Label(root, text="Mirror layers:").grid(column=1, row=9)
checkBox = tk.Checkbutton(root).grid(column=2, row=9) 

btn = tk.Button(root, text="Palletize!", command=palletizeClick).grid(column=2, row=10)

root.mainloop()