import tkinter as tk
import tkinter.ttk as ttk
import project
import CustomBox
import datahandler as dh


# lager ny label og inputfield
def newInput(root, msg, pos1, pos2):
    lbl = tk.Label(root, text=msg)
    lbl.grid(column=pos1, row=pos2, padx=2, pady=2)
    inpt = tk.Entry(root, width=10)
    inpt.grid(column=pos1+1, row=pos2, padx=2, pady=2)
    return inpt


class MainFrame:
    def __init__(self, master):
        master.title("UR10 Palletizing")
        self.frame = tk.Frame(master)

        self.label = tk.Label(master, text="Choose box:").grid(column=1, row=2, padx=2, pady=2)
        self.combo = ttk.Combobox(master, width=15)
        self.combo['values'] = dh.datahandler.getBoxes()
        self.combo.grid(column=2, row=2, padx=2, pady=2)

        self.btn = tk.Button(master, text="Add a custom box", command=self.addCustomBox).grid(column=2, row=3, padx=2, pady=2)

        self.targetLabel = tk.Label(master, text="Choose target:").grid(column=1, row=4, padx=2, pady=2)
        self.targetCombo = ttk.Combobox(master, width=15)
        self.targetCombo['values'] = ("Left target", "Rigth target")
        self.targetCombo.grid(column=2, row=4, padx=2, pady=2)

        self.inputArray = []

        self.inputArray.append( newInput(master, "Number of layers:", 1, 5) )
        self.inputArray.append( newInput(master, "Boxes in x direction on layer:", 1, 6) )
        self.inputArray.append( newInput(master, "Boxes in y direction on layer:", 1, 7) )
        self.inputArray.append( newInput(master, "Space between boxes:", 1, 8) )

        self.label2 = tk.Label(master, text="Mirror layers:").grid(column=1, row=9)
        self.checkBox = tk.Checkbutton(master).grid(column=2, row=9) 

        self.btn = tk.Button(master, text="Palletize!", command=self.palletizeClick).grid(column=2, row=10)

    
    def palletizeClick(self):
        boxObject = dh.datahandler.getBoxes()[self.combo.current()]
        target = self.targetCombo.current()
        boxes_in_z_dir = int(self.inputArray[0].get())
        boxes_in_x_dir = int(self.inputArray[1].get())
        boxes_in_y_dir = int(self.inputArray[2].get())
        space_between_boxes = int(self.inputArray[3].get())

        project.palletize(boxObject, target, boxes_in_x_dir, boxes_in_y_dir, boxes_in_z_dir, space_between_boxes)

    def addCustomBox(self):
        print("ikke implementert enda")





def main():
    root = tk.Tk()
    app = MainFrame(root)
    root.mainloop()

if __name__ == '__main__':
    main()