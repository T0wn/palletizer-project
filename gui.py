import tkinter as tk

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
inputArray.append( newInput(root, "Name of box to copy:", 1, 1) )
inputArray.append( newInput(root, "Box length:", 1, 2) )
inputArray.append( newInput(root, "Box width:", 1, 3) )
inputArray.append( newInput(root, "Box heigth:", 1, 4) )

btn = tk.Button(root, text="Palletize!", command=palletize)
btn.grid(column=2, row=5)

root.mainloop()