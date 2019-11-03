import tkinter as tk
import tkinter.ttk as ttk
import project

# lager ny label og inputfield
def newInput(root, msg, pos1, pos2):
    lbl = tk.Label(root, text=msg)
    lbl.grid(column=pos1, row=pos2, padx=0, pady=2)
    inpt = tk.Entry(root, width=10)
    inpt.grid(column=pos1+1, row=pos2, padx=0, pady=2)
    return inpt

def palletize():
    print(inputArray[0].get())



root = tk.Tk()
root.title("UR10 Palletizing")
# root.geometry("300x200")

grid = tk.Grid()

inputArray = []
# inputArray.append( newInput(root, "Name of box to copy:", 1, 1) )
# inputArray.append( newInput(root, "Box length:", 1, 2) )
# inputArray.append( newInput(root, "Box width:", 1, 3) )
# inputArray.append( newInput(root, "Box heigth:", 1, 4) )

label = tk.Label(root, text="Choose box:")
label.grid(column=1, row=4)
combo = ttk.Combobox(root, width=15)
combo['values'] = project.getBoxes()
combo.grid(column=2, row=4)

inputArray.append( newInput(root, "Boxes on pallet:", 1, 5) )
inputArray.append( newInput(root, "Boxes in x direction on layer:", 1, 6) )
inputArray.append( newInput(root, "Boxes in y direction on layer:", 1, 7) )

btn = tk.Button(root, text="Palletize!", command=palletize)
btn.grid(column=2, row=8)

root.mainloop()