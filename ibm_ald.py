import tkinter as tk
from tkinter import ttk as ttk
import json

posYDecode = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "J": 8, "K": 9, "L": 10, "M": 11, "N": 12}

ald_data = {}
aldText = ""

def fileLoad():
	with open(file.get()) as fh:
		global ald_data
		ald_data = json.load(fh)


def fileSave():
	json_object = json.dumps(ald_data, indent=4)
	with open(file.get(), "w") as fh:
			fh.write(json_object)

def renderALD():
	pagenum = page.get()
	if pagenum not in ald_data["pages"]:
		return
	aldWindow.delete('1.0', 'end')
	global aldText
	aldText = ""
	for y in range(103):
		for x in range(242):
			aldText = aldText + " "
		aldText = aldText + "\n"
	aldWindow.insert('end', aldText)

	for block in ald_data["pages"][pagenum]["BlockSN"]:
		pos = block["PrintPos"]
		posx = ((int(pos[0])-1) * 23) + 38
		posy = (posYDecode[pos[1]] * 7) + 3
		# Each block has a space of 23x7
		


window = tk.Tk()
window.title("IBM ALD Editor/Viewer")
window.geometry('1024x640')
topframe = tk.Frame(window)
topframe.pack(side = "top")
bottomframe = tk.Frame(window)
bottomframe.pack(side = "bottom")
lbl1 = tk.Label(topframe, text="File:")
lbl1.pack(side = "left")
file = tk.Entry(topframe, width=20)
file.pack(side = "left")
fileLoadButton = tk.Button(topframe, text="Load", command=fileLoad)
fileLoadButton.pack(side = "left")
fileSaveButton = tk.Button(topframe, text="Save", command=fileSave)
fileSaveButton.pack(side = "left")
page = tk.Entry(topframe, width=10)
page.pack(side = "left")
renderButton = tk.Button(topframe, text="Render", command=renderALD)
renderButton.pack(side = "left")
#text = tk.Text(bottomframe, font=('Andale Mono', 10), height=100, width=242, wrap = "none")
#text.pack(side = "bottom")
aldWindow = tk.Text(bottomframe, font=('Andale Mono', 12), height=104, width=242, wrap = "none")
ys = ttk.Scrollbar(bottomframe, orient = 'vertical', command = aldWindow.yview)
xs = ttk.Scrollbar(bottomframe, orient = 'horizontal', command = aldWindow.xview)
aldWindow['yscrollcommand'] = ys.set
aldWindow['xscrollcommand'] = xs.set
renderALD()
aldWindow.grid(column = 0, row = 0, sticky = 'nwes')
xs.grid(column = 0, row = 1, sticky = 'we')
ys.grid(column = 1, row = 0, sticky = 'ns')
bottomframe.grid_columnconfigure(0, weight = 1)
bottomframe.grid_rowconfigure(0, weight = 1)

window.mainloop()