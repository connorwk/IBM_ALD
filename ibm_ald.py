import tkinter as tk
from tkinter import ttk as ttk
import json
import platform
if platform.system() == "Windows":
	font = 'Lucida Console'
else:
	font = 'Andale Mono'

posYDecode = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "J": 8, "K": 9, "L": 10, "M": 11, "N": 12, "P": 13, "Q": 14, "R": 15, "S": 16, "T": 17, "U": 18, "V": 19, "W": 20, "X": 21, "Y": 22, "Z": 23}
posYEncode = ("A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z")


ald_data = {}
aldText = ""
# Used for routing to know if a block is populated.
block_pop = {}

def fileLoad():
	with open(file.get()) as fh:
		global ald_data
		ald_data = json.load(fh)


def fileSave():
	json_object = json.dumps(ald_data, indent=4)
	with open(file.get(), "w") as fh:
			fh.write(json_object)

def locOffset(loc):
	if str(loc).isnumeric():
		return int(loc)-1
	else:
		return posYDecode[loc]

# Returns the Block location code EX: 2B
# This is the 23x7 area a block is in
# We can compare to block_pop for routing around populated blocks
# We do however have to check the lower block if it has a name
def getBlockLoc(loc):
	posX = str((loc["x"]-38) // 23)
	posY = posYEncode[(loc["y"]-3) // 7]
	return (posX + posY)

# Returns the route location, which is where lines are routable
# EX Block vs Route Col: Route0, Block1, Route1, Block2, Route2...
def getRouteLoc(loc):
	col = (loc["x"]-38) // 23
	if ((loc["x"]-38) % 23) == 22:
		# On the output side so need to add 1 to col
		col = col + 1
	row = (loc["y"]-3) // 7
	loc["row"] = row
	loc["col"] = col
	return loc

def getXinBlock(loc):
	return ((loc["x"]-38) % 23)

def getYinBlock(loc):
	return(loc["y"]-3) % 7

# Returns the pin's x,y and route row,col
def getPinLoc(pagenum, blockSN, pinLoc):
	block = ald_data["pages"][pagenum]["BlockSN"][blockSN]
	pos = block["PrintPos"]
	piny = (locOffset(pos[1]) * 7) + 3 + locOffset(pinLoc)
	row = locOffset(pos[1])
	if str(pinLoc).isnumeric():
		pinx = (locOffset(pos[0]) * 23) + 38 + 22
		col = locOffset(pos[0]) + 1
	else:
		pinx = (locOffset(pos[0]) * 23) + 38 + 6
		col = locOffset(pos[0])
	
	return {"x":pinx, "y":piny, "row":row, "col":col}

def routeDown():
	return 0

def routeUp():
	return 0

def routeLeft():
	return 0

def routeRight():
	return 0

def routeTrace(startLoc, endLoc):
	currLoc = startLoc
	while currLoc != endLoc:
		while currLoc["row"] != endLoc["row"]:
			while currLoc["col"] != endLoc["col"]:
				nextLoc = currLoc
				nextLoc["x"] = nextLoc["x"] + 1
				if getBlockLoc(nextLoc) in block_pop:
					print("Hit populated block routing right")
					nextLoc = currLoc
					nextLoc["y"] = nextLoc["y"] + 1
				char = aldWindow.get(str(nextLoc["y"]) + "." + str(nextLoc["x"]), str(nextLoc["y"]+1) + "." + str(nextLoc["x"]))
				match char:
					case "┌":
						print("Hit trace routing right")
						nextLoc = currLoc
						nextLoc["y"] = nextLoc["y"] - 1
					case "└":
						print("Hit trace routing right")
						nextLoc = currLoc
						nextLoc["y"] = nextLoc["y"] + 1
					case "◊":
						print("Hit trace routing right")
						nextLoc = currLoc
						if getYinBlock(currLoc) <= 3:
							# Route Up
							print()
						else:
							# Route Down
							print()
						nextLoc["y"] = nextLoc["y"] + 1
					case "│":
						aldWindow.replace(str(nextLoc["y"]) + "." + str(nextLoc["x"]), str(nextLoc["y"]) + "." + str(nextLoc["x"]), "┼")

		print()
	return 0

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
		if block["Name"] != "":
			block_pop[pos] = 1
		else:
			block_pop[pos] = 0

		# Each block has a space of 23x7
		# Render Block
		for y in range(7):
			aldWindow.delete(str(posy+y) + "." + str(posx+9), str(posy+y) + "." + str(posx+16))
		if block["Name"] != "":
			aldWindow.replace(str(posy-1) + "." + str(posx+6), str(posy-1) + "." + str(posx+20), str(block["Name"]).center(14))
		aldWindow.insert(str(posy) + "." + str(posx+9), "┌──────┐")
		aldWindow.insert(str(posy+1) + "." + str(posx+9), "│" + str(block["Func"]).ljust(6) + "│")
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
					aldWindow.replace(str(posy+locOffset(ioLoc)) + "." + str(posx+17), str(posy+locOffset(ioLoc)) + "." + str(posx+20), "───")
				else:
					aldWindow.replace(str(posy+locOffset(ioLoc)) + "." + str(posx+17), str(posy+locOffset(ioLoc)) + "." + str(posx+20), io["Pin"])
				if io["Func"] != "":
					match io["Func"]:
						case 'i':
							aldWindow.replace(str(posy+locOffset(ioLoc)) + "." + str(posx+16), str(posy+locOffset(ioLoc)) + "." + str(posx+17), "◺")
						case _:
							aldWindow.replace(str(posy+locOffset(ioLoc)) + "." + str(posx+16), str(posy+locOffset(ioLoc)) + "." + str(posx+17), io["Func"])
			else:
				if io["Pin"] == "---":
					aldWindow.replace(str(posy+locOffset(ioLoc)) + "." + str(posx+6), str(posy+locOffset(ioLoc)) + "." + str(posx+9), "───")
				else:
					aldWindow.replace(str(posy+locOffset(ioLoc)) + "." + str(posx+6), str(posy+locOffset(ioLoc)) + "." + str(posx+9), io["Pin"])
				if io["Func"] != "":
					match io["Func"]:
						case 'i':
							aldWindow.replace(str(posy+locOffset(ioLoc)) + "." + str(posx+9), str(posy+locOffset(ioLoc)) + "." + str(posx+10), "◺")
						case _:
							aldWindow.replace(str(posy+locOffset(ioLoc)) + "." + str(posx+9), str(posy+locOffset(ioLoc)) + "." + str(posx+10), io["Func"])
	# Render OnPage Connections
	for blockSN in ald_data["pages"][pagenum]["Connections"]["OnPage"]:
		conn = ald_data["pages"][pagenum]["Connections"]["OnPage"][blockSN]
		for outLoc in conn:
			for toConnBlockSN in conn[outLoc]:
				startLoc = getPinLoc(pagenum, blockSN, outLoc)
				endLoc = getPinLoc(pagenum, toConnBlockSN, conn[outLoc][toConnBlockSN])
				#routeTrace(startLoc, endLoc)


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