import tkinter as tk
import tkinter.ttk as ttk
import project
import CustomBox
import datahandler as dh
import ast


# lager ny label og inputfield
def newInput(root, msg, pos1, pos2):
    lbl = tk.Label(root, text=msg)
    lbl.grid(column=pos1, row=pos2, padx=2, pady=2)
    inpt = tk.Entry(root, width=10)
    inpt.grid(column=pos1 + 1, row=pos2, padx=2, pady=2)
    return inpt


class MainFrame:
    def __init__(self, master):
        master.title("UR10 Palletizing")
        self.master = master
        self.frame = tk.Frame(master)

        self.label = tk.Label(master, text="Choose box:")
        self.label.grid(column=1, row=2, padx=2, pady=2)
        self.combo = ttk.Combobox(master, width=15)
        self.combo['values'] = dh.datahandler.getBoxes()
        self.combo.grid(column=2, row=2, padx=2, pady=2)

        self.btn = tk.Button(master, text="Add a custom box", command=self.addCustomBox)
        self.btn.grid(column=2, row=3, padx=2, pady=2)

        self.targetLabel = tk.Label(master, text="Choose target:")
        self.targetLabel.grid(column=1, row=10, padx=2, pady=2)
        testBox = ttk.Combobox(master, width=15)
        self.targetCombo = testBox
        self.targetCombo['values'] = ("Custom", "Left target", "Right target")
        self.targetCombo.grid(column=2, row=10, padx=2, pady=2)

        self.inputArray = []

        self.inputArray.append(newInput(master, "Number of layers:", 1, 5))
        self.inputArray.append(newInput(master, "Boxes in x direction on layer:", 1, 6))
        self.inputArray.append(newInput(master, "Boxes in y direction on layer:", 1, 7))
        self.inputArray.append(newInput(master, "Space between boxes:", 1, 8))

        self.label = tk.Label(master, text="X/Y/Z indent is only used on Custom target")
        self.label.grid(column=1, row=11, padx=2, pady=2)

        self.inputArray.append(newInput(master, "Target indentation in X", 1, 12))
        self.inputArray.append(newInput(master, "Target indentation in Y", 1, 13))
        self.inputArray.append(newInput(master, "Target indentation in Z", 1, 14))


        self.patternLabel = tk.Label(master, text="Layer pattern (optional):")
        self.patternLabel.grid(column=1, row=16)
        self.patternInput = tk.Text(master, height=4, width=30)
        self.patternInput.grid(column=2, row=16)

        self.label2 = tk.Label(master, text="Mirror layers:")
        self.label2.grid(column=1, row=17)

        self.checkVal = tk.BooleanVar()
        self.checkBox = tk.Checkbutton(master, var=self.checkVal)
        self.checkBox.grid(column=2, row=17)

        self.palletize_btn = tk.Button(master, text="Palletize!", command=self.palletizeClick)
        self.palletize_btn.grid(column=2, row=18)




    def updateComboBox(self):
        self.combo['values'] = dh.datahandler.getBoxes()

    def palletizeClick(self):
        boxObject = dh.datahandler.getBoxes()[self.combo.current()]
        target = self.targetCombo.current()
        boxes_in_z_dir = int(self.inputArray[0].get())
        boxes_in_x_dir = int(self.inputArray[1].get())
        boxes_in_y_dir = int(self.inputArray[2].get())
        space_between_boxes = int(self.inputArray[3].get())
        mirrored = self.checkVal.get()
        if self.targetCombo.current() == 0:
            plane_x_trans = int(self.inputArray[4].get())
            plane_y_trans = int(self.inputArray[5].get())
            plane_z_trans = int(self.inputArray[6].get())
            plane_cords = [plane_x_trans, plane_y_trans, plane_z_trans]

        patternText = self.patternInput.get("1.0", "end")

        # sjekker om textfeltet er tomt. Det er et linjeskift i feltet by default
        if (patternText != "\n"):
            pattern = self.parsePattern(patternText)
            if self.targetCombo.current() == 0:
                project.palletize(boxObject, target, boxes_in_x_dir, boxes_in_y_dir, boxes_in_z_dir, space_between_boxes, mirrored, layer_pattern=pattern, target_cords=plane_cords)
            else:
                project.palletize(boxObject, target, boxes_in_x_dir, boxes_in_y_dir, boxes_in_z_dir, space_between_boxes, mirrored, layer_pattern=pattern)
        else:
            if self.targetCombo.current() == 0:
                project.palletize(boxObject, target, boxes_in_x_dir, boxes_in_y_dir, boxes_in_z_dir, space_between_boxes, mirrored, target_cords=plane_cords)
            else:
                project.palletize(boxObject, target, boxes_in_x_dir, boxes_in_y_dir, boxes_in_z_dir, space_between_boxes, mirrored)

    # konverterer en string skrevet som en array til en array
    def parsePattern(self, patternText):
        return ast.literal_eval(patternText)

    def addCustomBox(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = newBoxFrame(self.newWindow, self)


class newBoxFrame:
    def __init__(self, master, mainFrame):
        self.master = master
        self.mainFrame = mainFrame
        self.frame = tk.Frame(master)

        self.inputArray = []
        self.inputArray.append(newInput(master, "name:", 1, 1))
        self.inputArray.append(newInput(master, "length:", 1, 2))
        self.inputArray.append(newInput(master, "width:", 1, 3))
        self.inputArray.append(newInput(master, "height:", 1, 4))

        self.addButton = tk.Button(master, text="Add box!", command=self.addBoxClick)
        self.addButton.grid(column=2, row=5, padx=60,pady=5)
        self.msgBox = tk.Label(master, text="")
        self.msgBox.grid(column=2, row=6)

    def addBoxClick(self):
        name = str(self.inputArray[0].get())
        length = int(self.inputArray[1].get())
        width = int(self.inputArray[2].get())
        height = int(self.inputArray[3].get())

        box = CustomBox.CustomBox(name, length, width, height)

        dh.datahandler.addBox(box)
        self.mainFrame.updateComboBox()
        self.msgBox = tk.Label(self.master, text="Box created!")
        self.msgBox.grid(column=2, row=6)


# Starter gui
def main():
    root = tk.Tk()
    app = MainFrame(root)
    root.mainloop()


if __name__ == '__main__':
    main()
