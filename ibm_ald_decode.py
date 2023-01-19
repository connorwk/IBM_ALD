import tkinter as tk
from tkinter import ttk as ttk
from PIL import Image, ImageTk
import json, os

circuit_data = {}
photos = {}

canvasXSize = 800
canvasYSize = 750

moduleIndex = 0
circnum = ""

window = tk.Tk()
window.title("IBM Circuit Number Decoder")
window.geometry('800x820')
topframe = tk.Frame(window)
topframe.pack(side = "top")
bottomcanvas = tk.Canvas(window, width=canvasXSize, height=canvasYSize)
bottomcanvas.pack(side = "bottom")
midframe = tk.Frame(window)
midframe.pack(side = "top")
lowframe = tk.Frame(window)
lowframe.pack(side = "top")

with open("ibm_circuit_info.json") as fh:
	circuit_data = json.load(fh)

for file in os.listdir("photos/"):
	if os.path.isfile(os.path.join("photos/", file)):
		if os.path.splitext(file)[1] == ".png":
			newimage = Image.open("photos/"+file)
			newimage.thumbnail((canvasXSize, canvasYSize), Image.Resampling.LANCZOS)
			photos[os.path.splitext(file)[0]] = ImageTk.PhotoImage(newimage)

def search():
	global moduleIndex
	moduleIndex = 0
	global circnum
	circnum = circuitnum.get()
	typechar = circnum[0]
	classnum = circnum[1:3]
	if typechar in circuit_data["type_dict"]:
		typebox.config(text=circuit_data["type_dict"][typechar])
	else:
		typebox.config(text="UNKNOWN")

	if classnum in circuit_data["class_dict"]:
		classbox.config(text=circuit_data["class_dict"][classnum])
	else:
		classbox.config(text="UNKNOWN")
	
	prevbutton.config(state="disabled")
	nextbutton.config(state="disabled")
	
	if circnum in circuit_data["circuit_dict"]:
		descbox.config(text=circuit_data["circuit_dict"][circnum]["desc"])
		modulelist = ""
		for module in circuit_data["circuit_dict"][circnum]["module"]:
			modulelist = modulelist + module + ", "
		modulelist = modulelist[:-2]
		modulesbox.config(text=modulelist)
		if circuit_data["circuit_dict"][circnum]["module"][0] != "":
			bottomcanvas.itemconfig(image_container, image=photos[circuit_data["circuit_dict"][circnum]["module"][0]])
			if len(circuit_data["circuit_dict"][circnum]["module"]) > 1:
				nextbutton.config(state="active")
		else:
			modulesbox.config(text="UNKNOWN")
			bottomcanvas.itemconfig(image_container, image=photos["unknown"])
	else:
		descbox.config(text="UNKNOWN")
		modulesbox.config(text="UNKNOWN")
		bottomcanvas.itemconfig(image_container, image=photos["unknown"])
	
	return 0

def nextbtn():
	global circnum
	global moduleIndex
	moduleIndex = moduleIndex + 1
	if moduleIndex == len(circuit_data["circuit_dict"][circnum]["module"])-1:
		nextbutton.config(state="disabled")
	prevbutton.config(state="active")
	bottomcanvas.itemconfig(image_container, image=photos[circuit_data["circuit_dict"][circnum]["module"][moduleIndex]])
	return 0
def prevbtn():
	global circnum
	global moduleIndex
	moduleIndex = moduleIndex - 1
	if moduleIndex == 0:
		prevbutton.config(state="disabled")
	nextbutton.config(state="active")
	bottomcanvas.itemconfig(image_container, image=photos[circuit_data["circuit_dict"][circnum]["module"][moduleIndex]])
	return 0

# "(.\d\d..)": "(.*)"
# "$1": {\n\t\t\t"desc": "$2",\n\t\t\t"photo": ""\n\t\t}


lbl1 = tk.Label(topframe, text="Circuit#:")
lbl1.pack(side = "left")
circuitnum = tk.Entry(topframe, width=6)
circuitnum.pack(side = "left")
searchbutton = tk.Button(topframe, text="Search", command=search)
searchbutton.pack(side = "left")
lbl2 = tk.Label(topframe, text="Type:")
lbl2.pack(side = "left")
typebox = tk.Label(topframe, text="")
typebox.pack(side = "left")

lbl3 = tk.Label(midframe, text="Class:")
lbl3.pack(side = "left")
classbox = tk.Label(midframe, text="")
classbox.pack(side = "left")
lbl4 = tk.Label(midframe, text="Description:")
lbl4.pack(side = "left")
descbox = tk.Label(midframe, text="")
descbox.pack(side = "left")

prevbutton = tk.Button(lowframe, text="Prev Module", command=prevbtn, state="disabled")
prevbutton.pack(side = "left")
nextbutton = tk.Button(lowframe, text="Next Module", command=nextbtn, state="disabled")
nextbutton.pack(side = "left")
lbl5 = tk.Label(lowframe, text="Module P/Ns:")
lbl5.pack(side = "left")
modulesbox = tk.Label(lowframe, text="")
modulesbox.pack(side = "left")

image_container = bottomcanvas.create_image(canvasXSize/2, canvasYSize/2, anchor='center', image=photos["unknown"])
window.mainloop()