import tkinter as tk
from tkinter import ttk as ttk
import json
import platform
if platform.system() == "Windows":
	font = 'Lucida Console'
else:
	font = 'Andale Mono'

posYDecode = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "J": 8, "K": 9, "L": 10, "M": 11, "N": 12, "P": 13, "Q": 14, "R": 15, "S": 16, "T": 17, "U": 18, "V": 19, "W": 20, "X": 21, "Y": 22, "Z": 23}

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
	if "pages" not in ald_data:
		return
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

	for blockSN in ald_data["pages"][pagenum]["BlockSN"]:
		block = ald_data["pages"][pagenum]["BlockSN"][blockSN]
		pos = block["PrintPos"]
		posx = ((int(pos[0])-1) * 23) + 38
		posy = (posYDecode[pos[1]] * 7) + 3
		# Each block has a space of 23x7
		# Render Block
		for y in range(7):
			aldWindow.delete(str(posy+y) + "." + str(posx+9), str(posy+y) + "." + str(posx+16))
		if block["Name"] != "":
			aldWindow.delete(str(posy+y) + "." + str(posx+9), str(posy-1) + "." + str(posx+16))
			aldWindow.insert(str(posy-1) + "." + str(posx+9), str(block["Name"]).center(8))
		aldWindow.insert(str(posy) + "." + str(posx+9), "┌──────┐")
		aldWindow.insert(str(posy+1) + "." + str(posx+9), "│" + block["Func"] + "│")
		aldWindow.insert(str(posy+2) + "." + str(posx+9), "│" + str(block["ACC"]).ljust(4) + str(block["SP"]).rjust(2) + "│")
		aldWindow.insert(str(posy+3) + "." + str(posx+9), "│" + str(block["CircuitNum"]).ljust(6) + "│")
		aldWindow.insert(str(posy+4) + "." + str(posx+9), "│" + str(block["CardType"]).ljust(4) + str(block["SubPortion"]).ljust(2) + "│")
		aldWindow.insert(str(posy+5) + "." + str(posx+9), "│" + str(block["Location"]).ljust(6) + "│")
		aldWindow.insert(str(posy+6) + "." + str(posx+9), "│" + block["PrintPos"] + "──" + blockSN + "│")
		# Render Block's IO
		for ioLoc in block["IO"]:
			io = block["IO"][ioLoc]
			if str(ioLoc).isnumeric():
				if io["Pin"] == "---":
					aldWindow.replace(str(posy+int(ioLoc)-1) + "." + str(posx+17), str(posy+int(ioLoc)-1) + "." + str(posx+20), "───")
				else:
					aldWindow.replace(str(posy+int(ioLoc)-1) + "." + str(posx+17), str(posy+int(ioLoc)-1) + "." + str(posx+20), io["Pin"])
				if io["Func"] != "":
					match io["Func"]:
						case 'i':
							aldWindow.replace(str(posy+int(ioLoc)-1) + "." + str(posx+16), str(posy+int(ioLoc)-1) + "." + str(posx+17), "◺")
						case _:
							aldWindow.replace(str(posy+int(ioLoc)-1) + "." + str(posx+16), str(posy+int(ioLoc)-1) + "." + str(posx+17), io["Func"])
			else:
				if io["Pin"] == "---":
					aldWindow.replace(str(posy+posYDecode[ioLoc]) + "." + str(posx+6), str(posy+posYDecode[ioLoc]) + "." + str(posx+9), "───")
				else:
					aldWindow.replace(str(posy+posYDecode[ioLoc]) + "." + str(posx+6), str(posy+posYDecode[ioLoc]) + "." + str(posx+9), io["Pin"])
				if io["Func"] != "":
					match io["Func"]:
						case 'i':
							aldWindow.replace(str(posy+posYDecode[ioLoc]) + "." + str(posx+9), str(posy+posYDecode[ioLoc]) + "." + str(posx+10), "◺")
						case _:
							aldWindow.replace(str(posy+posYDecode[ioLoc]) + "." + str(posx+9), str(posy+posYDecode[ioLoc]) + "." + str(posx+10), io["Func"])
	# Render PageIn Connections
	for conn in ald_data["pages"][pagenum]["Connections"]["PageIn"]:
		pos = conn["PrintPos"]
		row = (posYDecode[pos[0]] * 7) + 3
		posy = row + int(pos[1]) - 1
		aldWindow.replace(str(posy) + ".0", str(posy) + ".39", str(conn["Name"]).ljust(30,"─") + conn["Page"] + conn["SrcPin"])


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
file.insert("end", "test.json")
file.pack(side = "left")
fileLoadButton = tk.Button(topframe, text="Load", command=fileLoad)
fileLoadButton.pack(side = "left")
fileSaveButton = tk.Button(topframe, text="Save", command=fileSave)
fileSaveButton.pack(side = "left")
page = tk.Entry(topframe, width=10)
page.insert("end", "DN101")
page.pack(side = "left")
renderButton = tk.Button(topframe, text="Render", command=renderALD)
renderButton.pack(side = "left")
#text = tk.Text(bottomframe, font=('Andale Mono', 10), height=100, width=242, wrap = "none")
#text.pack(side = "bottom")
aldWindow = tk.Text(bottomframe, font=(font, 12), height=104, width=242, wrap = "none")
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