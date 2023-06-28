# This is the Editor. It is used by the user to create the game.
# Copyright (C) 2023 Marius Angermann
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import colorchooser
import os
import customtkinter as ctk
from PIL import Image
from PIL import ImageTk
import shutil
import subprocess
import sys
import re
from Export import Export


openfile = open("prcopen.info", "r")
readfile = openfile.readlines()
project_name = readfile[0]
openfile.close()

if project_name == "":
	sys.exit()

scenes = []

plattform = ""
if sys.platform.startswith('win'):
	plattform = "win"






#default costumtkinter setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
ctk.set_widget_scaling(1.5)  
app = ctk.CTk()
app.geometry("1920x1080")
app.after(0, lambda:app.state('zoomed'))
app.title("Artix Engine - Project:>" + project_name)
if plattform == "win":
	app.iconbitmap("src/icon.ico")

def openprcmanager():
	script_dir = os.path.dirname(os.path.realpath(__file__))
	subprocess.Popen('cmd /c cd /d "{}" &'.format(script_dir), shell=True)
	subprocess.Popen('python project_manager.py', shell=True)
	sys.exit()



#adding a menubar
menu_font = ("Arial", 12)
menu_bar = tk.Menu(app, font=menu_font)
app.config(menu=menu_bar)


#Creating the file Manager
file_manager_frame = ctk.CTkFrame(app,750,230,fg_color="#172a38",border_color="#000000")
file_manager_frame.pack()
file_manager_frame.place(x=270,y=430)

file_manager_heading = ctk.CTkFrame(app,750,30,border_width=0,fg_color="#2b2b2b",border_color="#000000")
file_manager_heading.pack()
file_manager_heading.place(x=270,y=430)

file_manager_label = ctk.CTkLabel(file_manager_heading, text="File Manager", fg_color="transparent")
file_manager_label.pack()
file_manager_label.place(relwidth=1,relheight=1)
file_manager_label.lift()

class Scene:
	def __init__(self,name="untitled",link=[]):
		self.name = name
		self.link = link
		self.objects = []
		camera = self.Camera2D()
		self.objects.append(camera)
	def add_object(self, type="", name=""):
		if type == "Sprite2D":
			self.objects.append(self.Sprite2D(name=name))
		scenetree.update()
	class Camera2D:
		def __init__(self):
			self.pos = [0,0]
			self.type = "Camera2D"
	class Sprite2D:
		def __init__(self, name="Untitled"):
			self.name = name
			self.type = "" 

class FileManager:
	def __init__(self):
		self.menu = tk.Menu(app, tearoff=0)
		self.menu.add_command(label="Delete", command=self.delete_file, font=("",15))
		self.displayed_files = []
		self.displayed_scenes = []
		self.files_list = []
		self.scenes_list = []
		self.button_file_map = {}
		self.FileLoader()
		self.dragged = False
		self.dragged_button = None
		self.scene_table = {}
	def secondinit(self, scenetree=None, viewport=None):
		self.scenetreelink = scenetree
		self.viewportlink = viewport

	def FileLoader(self):
		self.files_list.clear()
		openfile = open("projects/"+project_name+"/files.txt", "r")
		readfile = openfile.readlines()
		openfile.close()
		for lines in readfile:
			line = lines.rstrip("\n")
			self.files_list.append(line)

		openfile = open("projects/"+project_name+"/scenes.txt", "r")
		readfile = openfile.readlines()
		openfile.close()
		for lines in readfile:
			value = lines.rstrip("\n")
			if value != "":
				self.scenes_list.append(value)

	def open_scene(self, button):
		self.scenetreelink.general_update("load",self.scene_table[button])
		self.scenetreelink.select(self.scenetreelink.displayed_objects[0])
		self.viewportlink.update()
		#name1=self.scene_table[button]
		

	def display_files(self):
		currentindex = 0
		self.displayed_files = []
		lastbuttonpos = [-80,40]
		lastlabelpos = [-88,110]
		attempts = 0
		numberinline = 0
		newline = False
		for lines in self.files_list:
			testimg = ctk.CTkImage(dark_image=Image.open("src/icons/image_icon.png"),size=(50,60))
			button = ctk.CTkButton(file_manager_frame, text="", image=testimg, width=50, height=60)
			button.bind("<Button-3>", self.open_menu)
			button.bind("<ButtonPress-1>", lambda event, button=button: self.on_button_press(event, button))
			button.bind("<ButtonRelease-1>", self.on_button_release)
			name_label = ctk.CTkLabel(file_manager_frame, text=lines, fg_color="transparent")
			self.button_file_map[button] = lines
			self.displayed_files.append(testimg)
			self.displayed_files.append(button)
			self.displayed_files.append(name_label)
		self.scenes_list = list(set(self.scenes_list))
		for lines in self.scenes_list:
			testimg = ctk.CTkImage(dark_image=Image.open("src/icons/scene_icon.png"),size=(50,60))
			button = ctk.CTkButton(file_manager_frame, text="", image=testimg, width=50, height=60)
			self.scene_table[button] = lines
			button.bind("<Double-Button-1>", lambda event, button=button: self.open_scene(button))
			name_label = ctk.CTkLabel(file_manager_frame, text=lines, fg_color="transparent")
			self.displayed_scenes.append(button)
			self.displayed_scenes.append(name_label)
			

		for objects in self.displayed_files:
			if currentindex == 3:
				currentindex = 0
				attempts += 1
				numberinline += 1
			if currentindex == 0:
				if numberinline == 7:
					numberinline = 0
					attempts = 0
					newline = True
					lastbuttonpos = [10,lastbuttonpos[1]+100]
					lastlabelpos = [2,lastlabelpos[1]+100]
				currentindex += 1
				continue
			elif currentindex == 1:
				objects.pack(padx=0,pady=30)
				if attempts == 0:
					if newline:
						objects.place(x=lastbuttonpos[0],y=lastbuttonpos[1],relwidth=0.1,relheight=0.3)
					else:
						objects.place(x=10,y=40,relwidth=0.1,relheight=0.3)
						lastbuttonpos = [10,40]
				else:
					objects.place(x=lastbuttonpos[0]+100,y=lastbuttonpos[1],relwidth=0.1,relheight=0.3)
					lastbuttonpos = [lastbuttonpos[0]+100,lastbuttonpos[1]]
			elif currentindex == 2:
				objects.pack(padx=0,pady=30)
				if attempts == 0:
					if newline:
						objects.place(x=lastlabelpos[0],y=lastlabelpos[1],relwidth=0.12,relheight=0.07)
					else:
						objects.place(x=2,y=110,relwidth=0.12,relheight=0.07)
						lastlabelpos = [2,110]
				else:
					objects.place(x=lastlabelpos[0]+100,y=lastlabelpos[1],relwidth=0.12,relheight=0.07)
					lastlabelpos = [lastlabelpos[0]+100,lastlabelpos[1]]
			currentindex += 1

		attempts = 0
		currentindex = 0
		for objs in self.displayed_scenes:
			if numberinline == 7:
				newline = True
				lastbuttonpos = [10,lastbuttonpos[1]+100]
				lastlabelpos = [2,lastlabelpos[1]+100]
			else:
				newline = False

			if currentindex == 2:
				currentindex = 0
				numberinline += 1

			if currentindex == 0:
				objs.pack(padx=0,pady=30)
				objs.place(x=lastbuttonpos[0]+100,y=lastbuttonpos[1],relwidth=0.1,relheight=0.3)
				lastbuttonpos = [lastbuttonpos[0]+100,lastbuttonpos[1]]
			elif currentindex == 1:
				objs.pack(padx=0,pady=30)
				objs.place(x=lastlabelpos[0]+100,y=lastlabelpos[1],relwidth=0.12,relheight=0.07)
				lastlabelpos = [lastlabelpos[0]+100,lastlabelpos[1]]

			currentindex += 1

			



	def update(self):
		currentindex = 0
		for objects in self.displayed_files:
			if currentindex == 3:
				currentindex = 0
			if currentindex == 0:
				currentindex += 1
				continue
			objects.destroy()
			currentindex += 1
		for objects in self.displayed_scenes:
			objects.destroy()
		self.displayed_files.clear()
		self.displayed_scenes.clear()
		self.FileLoader()
		self.display_files()

	def binddelete(self):
		currentindex = 0
		attempts = 0
		for buttons in self.displayed_files:
			if currentindex == 3:
				currentindex = 0
				attempts += 1
			if currentindex == 0:
				currentindex += 1
				continue
			if currentindex == 1:
				currentindex += 1
				continue
			currentindex += 1
	def delete_file(self, file_name):
		openfile = open("projects/"+project_name+"/files.txt", "r")
		readfile = openfile.readlines()
		openfile.close()
		removed = []
		for lines in readfile:
			removed.append(lines.rstrip("\n"))
		removed.remove(file_name)
		writefile = open("projects/"+project_name+"/files.txt", "w")
		for lines in removed:
			if len(removed) > 1:
				writefile.writelines(lines+"\n")
			else:
				writefile.writelines(lines)
		writefile.close()
		self.update()

	def open_menu(self, event):
		label = event.widget
		button = label.master
		file = self.button_file_map[button]
		self.menu.entryconfig(0, command=lambda: self.delete_file(file))
		self.menu.post(event.x_root, event.y_root)

	def on_button_press(self, event, button):
		app.config(cursor="icon")
		self.dragged = True
		self.dragged_button = button

	def on_button_release(self, event):
		app.config(cursor="")
		


def import_file():
	filename = filedialog.askopenfilename(initialdir=os.path.expanduser("~/Documents"), title="Import File", filetypes=(("png files","*.png"),("jpeg files","*.jpg")))
	file_name = os.path.basename(filename)
	if file_name != "":
		with open("projects/"+project_name+"/files.txt", "r") as openfile:
			readfile = openfile.readlines()
			readfile.append(file_name.strip() + "\n")  
		with open("projects/"+project_name+"/files.txt", "w") as openfile:
			openfile.writelines(readfile)
		fm.update()
	shutil.copy(filename, "projects/"+project_name+"/Files/"+file_name)





file_manager_button = ctk.CTkButton(file_manager_heading, text="Import", command=import_file)
file_manager_button.pack()
file_manager_button.place(relwidth=0.2,relheight=1)







scenetreeframe = ctk.CTkFrame(app,width=265,height=420,border_width=0,fg_color="#666666")
scenetreeframe.pack()
scenetreeframe.place(x=2,y=10)

scenetreeheading = ctk.CTkFrame(app,width=265,height=40,border_width=0,fg_color="#3d3d3d",corner_radius=0)
scenetreeheading.pack()
scenetreeheading.place(x=2,y=4)

scenenamelabel = ctk.CTkLabel(scenetreeheading,text="DefaultScene",font=("",20))
scenenamelabel.pack()
scenenamelabel.place(x=20,y=0,relheight=1,relwidth=1)

scenetreecanvas = ctk.CTkCanvas(scenetreeframe,bg="#666666",scrollregion=(0, 0, 500, 1000))
scenetreecanvas.pack()
scenetreecanvas.place(x=0,y=0,relwidth=1,relheight=1)

hbar = ctk.CTkScrollbar(scenetreeframe,button_color="#a3a3a3")
hbar.pack()
hbar.place(x=250,y=30,relheight=0.93)


scenetreecanvas.configure(yscrollcommand=hbar.set)
hbar.configure(command=scenetreecanvas.yview)

def general_update(preset="startup",name1=""):
	scenes.clear()
	currentindex = 0
	scenetree.registeredscenes.clear()
	openfile = open("projects/"+project_name+"/scenes.txt", "r")
	readfile = openfile.readlines()
	openfile.close()
	for lines in readfile:
		scenetree.registeredscenes.append(lines.rstrip("\n"))
	scenes.clear()
	for i in scenetree.registeredscenes:
		scenetemp = Scene(i,link=scenes)
		scenes.append(scenetemp)
		openfile = open("projects/"+project_name+"/Scenes/"+i+".txt", "r")
		readfile = openfile.readlines()
		openfile.close()
		for objs in readfile:
			scenes[currentindex].objects.append(scenetemp.Sprite2D(objs))
		currentindex += 1
	if preset == "startup":
		scenetree.load_scene(scenetree.registeredscenes[0])
	elif preset == "load":
		scenetree.load_scene(name1)
	else:
		scenetree.load_scene(scenetree.currentscene)


class SceneTree:
	def __init__(self,link=[],general_update=[],properties1=[]):
		self.menu = tk.Menu(app, tearoff=0)
		self.menu.add_command(label="Delete", command=self.delete_object, font=("",15))
		self.button_file_map = {}
		self.general_update = general_update
		self.currentselected = "Camera2D"
		self.selected_object = None
		self.sceneslink = link
		self.properties_panel = properties1
		self.currentscene = ""
		self.displayed_objects = []
		self.registeredscenes = []
		openfile = open("projects/"+project_name+"/scenes.txt", "r")
		readfile = openfile.readlines()
		openfile.close()
		for lines in readfile:
			self.registeredscenes.append(lines.rstrip("\n"))

	def load_scene(self, name=""):
		for objects in self.displayed_objects:
			objects.destroy()
		self.displayed_objects.clear()


		search = 0
		self.currentscene = name
		currentscene = name
		for each in self.sceneslink:
			if each.name == name:
				search = self.sceneslink.index(each)
				self.currentsceneindex = search
				break
		scenenamelabel.configure(text=self.sceneslink[search].name)
		currentindex = 0
		lastpos = [25, 70]
		for each in self.sceneslink[search].objects:
			temp = []
			if each.type != "Camera2D":
				temp.append(each.name)
				var = temp[0].rstrip("\n")
			if each.type == "Camera2D":
				button = ctk.CTkButton(scenetreecanvas, text="Camera2D", font=("", 15), fg_color="#252626")
				button.configure(command=lambda button=button: self.select(button, "Camera2D"))
			else:
				button = ctk.CTkButton(scenetreecanvas, text=each.name.rstrip("\n"), font=("", 15), fg_color="#252626")
				button.configure(command=lambda button=button: self.select(button, each.name.rstrip("\n")))


			
			if each.type != "Camera2D":
				button.bind("<Button-3>", self.open_menu)
				self.button_file_map[button] = var
			self.displayed_objects.append(button)


			if currentindex == 0:
				button_width = int(scenetreecanvas.winfo_width() * 0.8)
				button_height = int(scenetreecanvas.winfo_height() * 0.1)
				button_window = scenetreecanvas.create_window(lastpos[0], lastpos[1], anchor="nw", width=button_width, height=button_height, window=button)
			else:
				button_width = int(scenetreecanvas.winfo_width() * 0.8)
				button_height = int(scenetreecanvas.winfo_height() * 0.1)
				button_window = scenetreecanvas.create_window(lastpos[0], lastpos[1] + 80, anchor="nw", width=button_width, height=button_height, window=button)
			if currentindex != 0:
				lastpos = [lastpos[0], lastpos[1] + 80]
			currentindex += 1
		canvas_width = scenetreecanvas.winfo_width()
		canvas_height = lastpos[1] + 60
		scenetreecanvas.configure(scrollregion=(0, 0, canvas_width, canvas_height))


	def select(self, object1=None, name="Camera2D", param="no"):

		if self.selected_object is not None or param == "yes":
			try:	
				self.selected_object.configure(fg_color="#252626")
			except:
				#happens when new object is created or existing deleted (I dont know why)
				pass
		if param == "no":
			object1.configure(fg_color="#a1a1a1")
			self.selected_object = object1
			self.selected_name = object1.cget("text")
			self.properties_panel.update()
		else:
			pass



		





	def update(self):
		for objects in self.displayed_objects:
			objects.destroy()
		self.displayed_objects.clear()
		self.load_scene(self.currentscene)
		self.select(self.displayed_objects[len(self.displayed_objects)-1])
		
		

	def delete_object(self, objectname=""): #objectname is for example player\n
		for scenes in self.sceneslink:
			if scenes.name == self.currentscene:
				for objs in scenes.objects:
					if objs.type != "Camera2D":
						if objs.name == objectname or objs.name == objectname+"\n":
							scenes.objects.remove(objs)
							break

		openfile = open("projects/"+project_name+"/Scenes/"+self.currentscene+".txt", "r")
		readfile = openfile.readlines()
		openfile.close()
		exlist = []
		exlist.append(objectname)
		readfile.remove(exlist[0].rstrip("\n")+"\n")


		os.remove("projects/"+project_name+"/Scenes/"+self.currentscene+"/"+exlist[0].rstrip("\n")+".config")

		writefile = open("projects/"+project_name+"/Scenes/"+self.currentscene+".txt", "w")
		for lines in readfile:
			writefile.writelines(lines)
		writefile.close()
		self.update()
		


	def open_menu(self, event):
		label = event.widget
		button = label.master
		objects = self.button_file_map[button]
		self.menu.entryconfig(0, command=lambda: self.delete_object(objects))
		self.menu.post(event.x_root, event.y_root)




def add_sprite():
	dialog = ctk.CTkInputDialog(text="Sprite Name:", title="Create Sprite")
	value = dialog.get_input()
	currentindex = 0
	for i in scenes:
		if scenetree.currentscene == i.name:
			break
		currentindex += 1
	if value != "":
		openfile = open("projects/"+project_name+"/Scenes/"+scenes[currentindex].name+".txt", "r")
		readfile = openfile.readlines()
		openfile.close()
		objectstemp = []
		for objs in readfile:
			objectstemp.append(objs.rstrip("\n"))
		objectstemp.append(value)
		writefile = open("projects/"+project_name+"/Scenes/"+scenes[currentindex].name+".txt", "w")
		for i in objectstemp:
			writefile.writelines(i+"\n")
		scenes[scenetree.currentsceneindex].objects.append(Scene.Sprite2D(value))
		spriteconfig = ["#TRANSFORM","200","200","180","180","#IMAGETEXTURE","none","#A-Physics","none","#A-Gravity","none","#A-Camerafollow","none"]
	with open("projects/"+project_name+"/Scenes/"+scenetree.currentscene+"/"+value+".config", "w") as f:
		for lines in spriteconfig:
			f.write(lines+"\n")
	with open("projects/"+project_name+"/Scenes/"+scenetree.currentscene+"/"+value+".es", "w") as f:
		f.write("")
	scenetree.update()





def add_menu(event):
	addmenu.post(addbutton.winfo_rootx(), addbutton.winfo_rooty() + addbutton.winfo_height())

addbutton = ctk.CTkButton(scenetreeheading, text="+", fg_color="#5f9467", font=("",20))
addbutton.pack()
addbutton.place(x=5,y=5,relwidth=0.2,relheight=0.7)

addmenu = tk.Menu(app, tearoff=0)
addmenu.add_command(label="Sprite",font=("",15),command=add_sprite)

addbutton.bind("<Button-1>", add_menu)

properties_panel_frame = ctk.CTkFrame(app,width=255,height=655,border_width=0,fg_color="#666666",corner_radius=0)
properties_panel_frame.pack()
properties_panel_frame.place(x=1022,y=4)

properties_panel_heading = ctk.CTkFrame(app,width=255,height=40,border_width=0,fg_color="#3d3d3d",corner_radius=0)
properties_panel_heading.pack()
properties_panel_heading.place(x=1022,y=4)

properties_panel_canvas = ctk.CTkCanvas(properties_panel_frame,bg="#666666")
properties_panel_canvas.pack()
properties_panel_canvas.place(x=0,y=0,relwidth=1,relheight=1)

properties_panel_label = ctk.CTkLabel(properties_panel_heading,text="Properties",font=("",22), anchor="w")
properties_panel_label.pack()
properties_panel_label.place(x=20,y=0,relwidth=1,relheight=1)

class Properties:
	def __init__(self):
		self.currentobject = ""
		self.objx = 0
		self.objy = 0
		self.objecttype = ""
		self.displayed_objects = []
		self.scenetreelink = None
		self.bg_color = ""
		self.touch = False
		self.frame1 = None
	def assign(self,viewportlink=None):
		self.viewportlink = viewportlink
	def update(self):
		self.currentobject = self.scenetreelink.selected_name
		for objects in self.displayed_objects:
			try:
				objects.destroy()
			except:
				pass
		self.displayed_objects = []
		self.displayed_objects.clear()

		openfile = open("projects/"+project_name+"/Scenes/"+self.scenetreelink.currentscene+"/"+self.scenetreelink.selected_name+".config","r")
		readfile = openfile.readlines()
		openfile.close()
		objecttemp = []
		for lines in readfile:
			objecttemp.append(lines.rstrip("\n"))

		transx = float(objecttemp[1])
		transy = float(objecttemp[2])
		transx = int(transx)
		transy = int(transy)

		if self.scenetreelink.selected_name != "Camera2D":
			scalex = float(objecttemp[3])
			scaley = float(objecttemp[4])
			scalex = int(scalex)
			scaley = int(scaley)

		self.bg_color = objecttemp[4]

		self.objx = transx
		self.objy = transy

		transformlabel = ctk.CTkLabel(properties_panel_canvas, text="Position:", font=("",20))
		transformlabel.pack()
		transformlabel.place(x=10,y=0,relwidth=0.4,relheight=0.2)
		self.displayed_objects.append(transformlabel)
		xlabel = ctk.CTkLabel(properties_panel_canvas, text="X:", font=("",18))
		xlabel.pack()
		xlabel.place(x=20,y=85,relwidth=0.1,relheight=0.045)
		self.displayed_objects.append(xlabel)
		xentry = ctk.CTkEntry(properties_panel_canvas)
		xentry.insert(0, str(transx))
		xentry.pack()
		xentry.place(x=50,y=85,relwidth=0.15)
		self.displayed_objects.append(xentry)
		ylabel = ctk.CTkLabel(properties_panel_canvas, text="Y:", font=("",18))
		ylabel.pack()
		ylabel.place(x=90,y=85,relwidth=0.1,relheight=0.045)
		self.displayed_objects.append(ylabel)
		yentry = ctk.CTkEntry(properties_panel_canvas)
		yentry.insert(0, str(transy))
		yentry.pack()
		yentry.place(x=120,y=85,relwidth=0.15)
		self.displayed_objects.append(yentry)

		if self.scenetreelink.selected_name != "Camera2D":
			scalelabel = ctk.CTkLabel(properties_panel_canvas, text="Scale:", font=("",20))
			scalelabel.place(x=22,y=130)
			self.displayed_objects.append(scalelabel)
			xscalelabel = ctk.CTkLabel(properties_panel_canvas, text="X:", font=("",18))
			xscalelabel.place(x=20,y=165,relwidth=0.1,relheight=0.045)
			self.displayed_objects.append(xscalelabel)
			xscale = ctk.CTkEntry(properties_panel_canvas)
			xscale.insert(0, str(scalex))
			xscale.place(x=50,y=165,relwidth=0.15)
			self.displayed_objects.append(xscale)
			yscalelabel = ctk.CTkLabel(properties_panel_canvas, text="Y:", font=("",18))
			yscalelabel.place(x=90,y=165,relwidth=0.1,relheight=0.045)
			self.displayed_objects.append(yscalelabel)
			yscale = ctk.CTkEntry(properties_panel_canvas)
			yscale.insert(0, str(scaley))
			yscale.place(x=120,y=165,relwidth=0.15)
			self.displayed_objects.append(yscale)

		if self.scenetreelink.selected_name == "Camera2D":
			colorlabel = ctk.CTkLabel(properties_panel_canvas, text="Background Color", font=("",20))
			colorlabel.pack()
			colorlabel.place(x=10,y=125,relwidth=0.65,relheight=0.05)
			self.displayed_objects.append(colorlabel)
			colorpreview = ctk.CTkFrame(properties_panel_canvas, width=100, height=35, fg_color=objecttemp[4])
			colorpreview.pack()
			colorpreview.place(x=20,y=165)
			self.displayed_objects.append(colorpreview)
			if plattform == "win":
				changebutton = ctk.CTkButton(properties_panel_canvas, text="     🖊️", font=("",20), command=self.pick_color)
			else:
				changebutton = ctk.CTkButton(properties_panel_canvas, text="🖊️", font=("",20), command=self.pick_color)
			changebutton.pack()
			changebutton.place(x=120,y=165,relwidth=0.15,relheight=0.055)
			self.displayed_objects.append(changebutton)
		else:
			imagelabel = ctk.CTkLabel(properties_panel_canvas, text="Image Texture", font=("",20))
			imagelabel.pack()
			imagelabel.place(x=15,y=210,relwidth=0.55,relheight=0.05)
			self.displayed_objects.append(imagelabel)
			imagepreview = ctk.CTkFrame(properties_panel_canvas, width=100, height=100, fg_color="#ffffff")
			imagepreview.pack()
			imagepreview.place(x=25,y=255)
			self.frame1 = imagepreview
			self.displayed_objects.append(imagepreview)
			
			if objecttemp[6] == "none":
				previewlabel = ctk.CTkLabel(imagepreview, text="no texture", text_color="#8a8a8a", font=("",15))
				previewlabel.pack()
				previewlabel.place(relwidth=1,relheight=1)
				self.displayed_objects.append(previewlabel)
			else:
				previewimage = ctk.CTkImage(dark_image=Image.open("projects/"+project_name+"/Files/"+objecttemp[6]),size=(80,80))
				previewlabel = ctk.CTkLabel(imagepreview, image=previewimage, text="")
				previewlabel.pack()
				previewlabel.place(relwidth=1,relheight=1)
				self.displayed_objects.append(previewlabel)
		self.viewportlink.update()

	def inframe(self):
		searched = self.displayed_objects[self.displayed_objects.index(self.frame1)]
		frame_x = searched.winfo_rootx()
		frame_y = searched.winfo_rooty()
		frame_width = searched.winfo_width()
		frame_height = searched.winfo_height()
		cursor_x = app.winfo_pointerx()
		cursor_y = app.winfo_pointery()

		if frame_x <= cursor_x <= frame_x + frame_width and frame_y <= cursor_y <= frame_y + frame_height:
			return True
		else:
			return False


	def apply(self):
		openfile = open("projects/"+project_name+"/Scenes/"+self.scenetreelink.currentscene+"/"+self.scenetreelink.selected_name+".config","r")
		readfile = openfile.readlines()
		openfile.close()
		objecttemp = []
		for lines in readfile:
			objecttemp.append(lines.rstrip("\n"))

		if re.match(r'^\d+$', self.displayed_objects[2].get()) and re.match(r'^\d+$', self.displayed_objects[4].get()):
			objecttemp[1] = self.displayed_objects[2].get()
			objecttemp[2] = self.displayed_objects[4].get()

			if self.scenetreelink.selected_name == "Camera2D":
				objecttemp[4] = self.bg_color

			writefile = open("projects/"+project_name+"/Scenes/"+self.scenetreelink.currentscene+"/"+self.scenetreelink.selected_name+".config","w")
			for lines in objecttemp:
				writefile.writelines(lines+"\n")
			writefile.close()
		else:
			messagebox.showwarning("Warning", "Position value is not valid!")

		if self.scenetreelink.selected_name != "Camera2D":
			if re.match(r'^\d+$', self.displayed_objects[7].get()) and re.match(r'^\d+$', self.displayed_objects[9].get()):
				objecttemp[3] = self.displayed_objects[7].get()
				objecttemp[4] = self.displayed_objects[9].get()

				writefile = open("projects/"+project_name+"/Scenes/"+self.scenetreelink.currentscene+"/"+self.scenetreelink.selected_name+".config","w")
				for lines in objecttemp:
					writefile.writelines(lines+"\n")
				writefile.close()
			else:
				messagebox.showwarning("Warning", "Scale value is not valid!")


		self.viewportlink.update()



		self.update()
	def pick_color(self):
		fbg_color = colorchooser.askcolor()[1]
		if fbg_color != None:
			self.bg_color = fbg_color
			self.displayed_objects[6].configure(fg_color=self.bg_color)

def build_game():
	def copy_files(source_dir, destination_dir):
		file_list = os.listdir(source_dir)
		for file_name in file_list:
			source_path = os.path.join(source_dir, file_name)
			destination_path = os.path.join(destination_dir, file_name)
			shutil.copy2(source_path, destination_path)

	try:
		os.remove("projects/"+project_name+"/build")
	except:
		pass
	directory_path = "projects/"+project_name+"/build"
	os.makedirs(directory_path, exist_ok=True)

	directory_path = "projects/"+project_name+"/build/src"
	os.makedirs(directory_path, exist_ok=True)

	copy_files("projects/"+project_name+"/Files", "projects/"+project_name+"/build/src")
	shutil.copy2("Engine.py", "projects/"+project_name+"/build")

	exporter = Export(project_name)
	exporter.build()

	relative_path = "projects/"+project_name+"/build/main.py"
	absolute_path = os.path.abspath(relative_path)
	file_dir = os.path.dirname(absolute_path)

	subprocess.Popen(['python', absolute_path], cwd=file_dir)








viewport_canvas = ctk.CTkCanvas(app,width=1100,height=630)
viewport_canvas.place(x=415,y=5)
#viewport_canvas.configure(scrollregion=(-1000, -1000, 1000, 1000))
#viewport_canvas.configure(xscrollincrement='1', yscrollincrement='1')



play_button = ctk.CTkButton(viewport_canvas,text="Play",command=build_game,corner_radius=0, fg_color="#49bf51", font=("",20))
play_button.place(x=625,y=0,relwidth=0.15,relheight=0.1)

#viewporttools = ctk.CTkSegmentedButton(viewport_canvas,values=["Move","Scale","Rotate"])
#viewporttools.pack()
#viewporttools.place(x=0,y=45)


class Viewport:
	def __init__(self, scenetreelink=None):
		self.displayed_objects = []
		self.scenetreelink = scenetreelink
		self.imagetks = []
		self.drag_data = {'x': 0, 'y': 0, 'item_id': None}
		self.currentitem = None
		self.itemtable = {}
		self.selected_item_id = None
		self.outline_color = 'blue'
		self.outline_width = 2


	def start_drag(self, event):
		item_id = event.widget.find_closest(event.x, event.y)
		self.drag_data['item_id'] = item_id[0]

		# Get the bounding box of the object
		bbox = event.widget.bbox(item_id[0])

		# Calculate the middle position of the object
		middle_x = (bbox[0] + bbox[2]) / 2
		middle_y = (bbox[1] + bbox[3]) / 2

		# Set the cursor position to the middle of the object
		self.drag_data['x'] = middle_x
		self.drag_data['y'] = middle_y


		self.selected_item_id = item_id[0]




		


	def drag(self, event):
		dx = event.x - self.drag_data['x']
		dy = event.y - self.drag_data['y']
		event.widget.move(self.drag_data['item_id'], dx, dy)
		self.drag_data['x'] = event.x
		self.drag_data['y'] = event.y

	def stop_drag(self, event):
		self.drag_data['x'] = event.x
		self.drag_data['y'] = event.y
		x = self.drag_data["x"]
		y = self.drag_data["y"]
		name = self.itemtable[self.drag_data['item_id']].rstrip("\n")

		if self.selected_item_id is not None:
			viewport_canvas.delete('outline')

		self.selected_item_id = self.drag_data['item_id']

		bbox = viewport_canvas.bbox(self.selected_item_id)

		outline_id = viewport_canvas.create_rectangle(
			bbox[0], bbox[1], bbox[2], bbox[3],
			outline=self.outline_color, width=self.outline_width, tags='outline'
		)

		viewport_canvas.tag_raise(outline_id)
		self.drag_data = {'x': 0, 'y': 0, 'item_id': None}

		old_width = 1100
		old_height = 630

		new_width = 800
		new_height = 600

		old_x = int(x)
		old_y = int(y)


		openfile = open("projects/"+project_name+"/Scenes/"+self.scenetreelink.currentscene+"/"+name+".config", "r")
		readfile = openfile.readlines()
		openfile.close()
		objecttemp = []
		for lines in readfile:
			objecttemp.append(lines.rstrip("\n"))

		objecttemp[1] = str(old_x)
		objecttemp[2] = str(old_y)

		writefile = open("projects/"+project_name+"/Scenes/"+self.scenetreelink.currentscene+"/"+name+".config", "w")
		for lines in objecttemp:
			writefile.writelines(lines+"\n")
		writefile.close()

		self.properties.update()

		for objects in self.scenetreelink.displayed_objects:
			text = objects.cget("text")
			if text == name:
				index = self.scenetreelink.select(self.scenetreelink.displayed_objects[self.scenetreelink.displayed_objects.index(objects)], "nk")
				break

	def secondinit(self, propertieslink=None):
		self.properties = propertieslink

	def update(self, name1=""):
		for objects in self.displayed_objects:
			objects.destroy()
		self.displayed_objects.clear()
		self.imagetks.clear()

		generalopen = open("projects/"+project_name+"/Scenes/"+self.scenetreelink.currentscene+"/Camera2D.config", "r")
		generalread = generalopen.readlines()
		generalopen.close()
		objecttemp = []
		for lines in generalread:
			objecttemp.append(lines.rstrip("\n"))
		color = objecttemp[4]
		viewport_canvas.configure(bg=color)

		searched = 0
		for differentscenes in scenes:
			if name1 == "":
				if differentscenes.name == self.scenetreelink.currentscene:
					searched = scenes.index(differentscenes)
					break
			else:
				if differentscenes.name == name1:
					searched = scenes.index(differentscenes)
					break
		currentindex = 0
		gap = False
		for objs in scenes[searched].objects:
			if currentindex == 0:
				currentindex += 1
				continue

			
			if objs.name != "":
				openfile = open("projects/"+project_name+"/Scenes/"+self.scenetreelink.currentscene+"/"+objs.name.rstrip("\n")+".config", "r")
			else:
				continue
			
			readfile = openfile.readlines()
			openfile.close()
			objecttemp = []
			for lines in readfile:
				objecttemp.append(lines.rstrip("\n"))

			posx = objecttemp[1]
			posy = objecttemp[2]

			game_width = 800
			game_height = 600
			editor_width = 1100
			editor_height = 630

			game_x = float(posx)
			game_y = float(posy)


			x_scale = editor_width / game_width
			y_scale = editor_height / game_height

			editor_x = game_x
			editor_y = game_y

			if objecttemp[6] == "none": 
				pass
			else:
				image0 = Image.open("projects/"+project_name+"/Files/"+objecttemp[6])
				image1 = image0.resize((int(objecttemp[3]),int(objecttemp[4])))
				image_tk = ImageTk.PhotoImage(image1)
				self.imagetks.append(image_tk)

				item_id = viewport_canvas.create_image(editor_x, editor_y, image=image_tk,tags="image")
				self.itemtable[item_id] = objs.name
				viewport_canvas.tag_bind(item_id, '<ButtonPress-1>', self.start_drag)
				viewport_canvas.tag_bind(item_id, '<B1-Motion>', self.drag)
				viewport_canvas.tag_bind(item_id, '<ButtonRelease-1>', self.stop_drag)
			


fm = FileManager()
fm.display_files()
fm.update()



properties_panel = Properties()
scenetree = SceneTree(link=scenes,general_update=general_update,properties1=properties_panel)
viewport = Viewport(scenetree)
properties_panel.assign(viewport)
viewport.secondinit(properties_panel)

fm.secondinit(scenetree, viewport)



def EventSystemWindow():
	if scenetree.selected_name == "Camera2D":
		messagebox.showwarning("Warning", "Camera2D cant have Event System")
		return True
	root = ctk.CTk()
	root.geometry("800x600")
	root.title("Event System")
	if plattform == "win":
		root.iconbitmap("src/icon.ico")
	shown_widgets = []

	

	event_system_canvas = ctk.CTkCanvas(root,width=795,height=500,bg="#292929")
	event_system_canvas.place(x=0,y=91)
	cscrollbar = ctk.CTkScrollbar(root, command=event_system_canvas.yview)
	cscrollbar.place(relx=1, rely=0.15, relheight=0.85, anchor='ne')
	event_system_canvas.configure(yscrollcommand=cscrollbar.set)

	def on_canvas_mousewheel(event):
		event_system_canvas.yview_scroll(-1 * int(event.delta/120), "units")

	event_system_canvas.bind_all("<MouseWheel>", on_canvas_mousewheel)

	class Event_OR_Action:
		def __init__(self, own_type="event", parameter1="keypress",arguments=['Space'],evindex=0,acindex=0, lastframepos=60, function=None):
			self.displayed_objects = []
			self.lastframepos = lastframepos
			self.type = own_type
			self.param = parameter1
			self.args = arguments
			self.func = function
			if self.type == "event":
				self.event_index = evindex
				self.create_event()
			if self.type == "action":
				self.event_index = evindex
				self.create_action()
				self.action_index = acindex
		def get(self):
			if self.type == "event":
				if self.param == "keypress" or self.param == "keyhold":
					value = "event+"+self.param+"+"+self.optionmenu1.get()
					return value
				elif self.param == "colwith":
					value = "event+colwith+"+self.optionmenu1.get()
					return value
				elif self.param == "colbtw":
					value = "event+colbtw+"+self.optionmenu1.get()+"+"+self.optionmenu2.get()
					return value

			elif self.type == "action":
				if self.param == "setpos" or self.param == "move" or self.param == "applyforce":
					value = "action+"+self.param+"+"+self.xentry.get()+"+"+self.yentry.get()
					return value
				elif self.param == "setobjpos" or self.param == "moveobj":
					value = "action+"+self.param+"+"+self.optionmenu1.get()+"+"+self.xentry.get()+"+"+self.yentry.get()
					return value
				elif self.param == "loadscene":
					value = "action+loadscene+"+self.optionmenu1.get()
					return value

		def add_menu(self,event):
			self.addactionmenu.post(self.plus_button.winfo_rootx(), self.plus_button.winfo_rooty() + self.plus_button.winfo_height())
		def delete_event(self):
			searched_object = scenetree.selected_name
			scene = scenetree.currentscene
			openfile = open("projects/"+project_name+"/Scenes/"+scene+"/"+searched_object+".es", "r")
			readfile = openfile.readlines()
			openfile.close()
			objecttemp = []
			for lines in readfile:
				value = lines.rstrip("\n")
				if value != "":
					objecttemp.append(value)
			newtemp = []
			eventcounter = 0
			found = False
			for i in objecttemp:
				value = i.split("+")

				#capturing events
				if value[0] == "event":
					if found == True:
						found = False
					eventcounter += 1
					if (eventcounter-1) == self.event_index:
						found = True
						continue
					else:
						newtemp.append(i)

				#capturing actions
				if value[0] == "action":
					if found == False:
						newtemp.append(i)



			writefile = open("projects/"+project_name+"/Scenes/"+scene+"/"+searched_object+".es", "w")
			for lines in newtemp:
				writefile.writelines(lines+"\n")
			writefile.close()
			self.func()

		def delete_action(self):
			searched_object = scenetree.selected_name
			scene = scenetree.currentscene
			openfile = open("projects/"+project_name+"/Scenes/"+scene+"/"+searched_object+".es", "r")
			readfile = openfile.readlines()
			openfile.close()
			objecttemp = []
			for lines in readfile:
				value = lines.rstrip("\n")
				if value != "":
					objecttemp.append(value)
			newtemp = []

			eventindex = -1
			last = ""
			actionindex = -1
			found = False
			done = False
			for i in objecttemp:
				value = i.split("+")
				if eventindex == self.event_index and actionindex == self.action_index:
					if value[0] != "event":
						if done == False:
							done = True
							continue
				if value[0] == "event":
					actionindex = 0
					eventindex += 1
				elif value[0] == "action":
					actionindex += 1
				newtemp.append(i)

			writefile = open("projects/"+project_name+"/Scenes/"+scene+"/"+searched_object+".es", "w")
			for lines in newtemp:
				writefile.writelines(lines+"\n")
			writefile.close()
			self.func()

		def add_action(self, type1=""):
			string = ""
			if type1 == "setpos":
				string = "action+setpos+0+0"
			elif type1 == "move":
				string = "action+move+0+0"
			elif type1 == "setobjpos":
				string = "action+setobjpos+"+scenetree.selected_name+"+0+0"
			elif type1 == "moveobj":
				string = "action+moveobj+"+scenetree.selected_name+"+0+0"
			elif type1 == "applyforce":
				string = "action+applyforce+0+0"
			elif type1 == "loadscene":
				string = "action+loadscene+"+scenetree.currentscene
			searched_object = scenetree.selected_name
			scene = scenetree.currentscene
			openfile = open("projects/"+project_name+"/Scenes/"+scene+"/"+searched_object+".es", "r")
			readfile = openfile.readlines()
			openfile.close()
			objecttemp = []
			for lines in readfile:
				value = lines.rstrip("\n")
				if value != "":
					objecttemp.append(value)
			newtemp = []

			eventindex = 0
			done = False
			for lines in objecttemp:
				newtemp.append(lines)
				value = lines.split("+")
				if eventindex == self.event_index:
					if done == False:
						if value[0] == "event":
							newtemp.append(string)
							done = True
				if value[0] == "event":
					eventindex += 1

			writefile = open("projects/"+project_name+"/Scenes/"+scene+"/"+searched_object+".es", "w")
			for lines in newtemp:
				writefile.writelines(lines+"\n")
			writefile.close()

			self.func()

		def create_event(self):
			self.frame = ctk.CTkFrame(event_system_canvas, width=475, height=35, fg_color="#525252")
			event_system_canvas.create_window(30, self.lastframepos, window=self.frame, anchor='nw')
			self.addactionmenu = tk.Menu(root, tearoff=0)
			self.addactionmenu.add_separator()
			self.addactionmenu.add_command(label="Set Position",font=("",15), command=lambda:self.add_action("setpos"))
			self.addactionmenu.add_separator()
			self.addactionmenu.add_command(label="Move",font=("",15), command=lambda:self.add_action("move"))
			self.addactionmenu.add_separator()
			self.addactionmenu.add_command(label="Set Object Position",font=("",15), command=lambda:self.add_action("setobjpos"))
			self.addactionmenu.add_separator()
			self.addactionmenu.add_command(label="Move Object",font=("",15), command=lambda:self.add_action("moveobj"))
			self.addactionmenu.add_separator()
			self.addactionmenu.add_command(label="Apply Force",font=("",15),command=lambda:self.add_action("applyforce"))
			self.addactionmenu.add_separator()
			self.addactionmenu.add_command(label="Load Scene",font=("",15),command=lambda:self.add_action("loadscene"))
		
			if self.type == "event":
				evtype = "KEYPRESS"
				if self.param == "keypress":
					evtype = "KEYPRESS"
				elif self.param == "keyhold":
					evtype = "KEYHOLD"
				elif self.param == "colwith":
					evtype = "COLLISION WITH"
				elif self.param == "colbtw":
					evtype = "COLLISION"
				label = ctk.CTkLabel(self.frame, text="Event: "+evtype,font=("",19))
				if self.param == "colwith":
					label.place(x=-30,y=2,relwidth=0.6,relheight=0.9)
				else:
					label.place(x=-10,y=2,relwidth=0.4,relheight=0.9)

				if self.param == "keypress" or self.param == "keyhold":
					self.optionmenu1 = ctk.CTkOptionMenu(self.frame,fg_color="#878787",button_color="#333333", values=['Space', 'UP', 'DOWN', 'LEFT', 'RIGHT', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])
					self.optionmenu1.place(x=190,y=2.5,relwidth=0.2,relheight=0.8)
					self.optionmenu1.set(self.args[0])
					self.displayed_objects.append(self.optionmenu1)
				elif self.param == "colwith":
					searched_object = scenetree.selected_name
					scene = scenetree.currentscene
					openfile = open("projects/"+project_name+"/Scenes/"+scene+".txt", "r")
					readfile = openfile.readlines()
					openfile.close()
					objecttemp = []
					for lines in readfile:
						value = lines.rstrip("\n")
						if value != "":
							objecttemp.append(value)
					try:
						objecttemp.remove(searched_object)
					except:
						pass

					self.optionmenu1 = ctk.CTkOptionMenu(self.frame,fg_color="#878787",button_color="#333333", values=objecttemp)
					self.optionmenu1.place(x=230,y=2.5,relwidth=0.2,relheight=0.8)
					self.optionmenu1.set(self.args[0])
					self.displayed_objects.append(self.optionmenu1)

				elif self.param == "colbtw":
					searched_object = scenetree.selected_name
					scene = scenetree.currentscene
					openfile = open("projects/"+project_name+"/Scenes/"+scene+".txt", "r")
					readfile = openfile.readlines()
					openfile.close()
					objecttemp = []
					for lines in readfile:
						value = lines.rstrip("\n")
						if value != "":
							objecttemp.append(value)

					self.optionmenu1 = ctk.CTkOptionMenu(self.frame,fg_color="#878787",button_color="#333333", values=objecttemp)
					self.optionmenu1.place(x=175,y=2.5,relwidth=0.2,relheight=0.8)
					self.optionmenu1.set(self.args[0])
					self.displayed_objects.append(self.optionmenu1)

					self.optionmenu2 = ctk.CTkOptionMenu(self.frame,fg_color="#878787",button_color="#333333", values=objecttemp)
					self.optionmenu2.place(x=275,y=2.5,relwidth=0.2,relheight=0.8)
					self.optionmenu2.set(self.args[1])
					self.displayed_objects.append(self.optionmenu2)

			self.plus_button = ctk.CTkButton(self.frame, fg_color="#65a36d",text="+", font=("",20))
			self.plus_button.place(x=380,y=1,relwidth=0.09,relheight=0.9)
			self.displayed_objects.append(self.plus_button)
			self.plus_button.bind("<Button-1>", self.add_menu)

			self.del_button = ctk.CTkButton(self.frame, fg_color="#ff4040",text="X", font=("",19),command=self.delete_event)
			self.del_button.place(x=435,y=1,relwidth=0.08,relheight=0.9)
			self.displayed_objects.append(self.del_button)

		def create_action(self):
			self.frame = ctk.CTkFrame(event_system_canvas, width=430,height=35,fg_color="#094e4f")
			event_system_canvas.create_window(75, self.lastframepos, window=self.frame, anchor='nw')

			evtype = "move"
			if self.param == "setpos":
				evtype = "Set Position"
			elif self.param == "move":
				evtype = "Move"
			elif self.param == "setobjpos":
				evtype = "Set OBJ Position"
			elif self.param == "moveobj":
				evtype = "Move Object"
			elif self.param == "applyforce":
				evtype = "Apply Force"
			elif self.param == "loadscene":
				evtype = "Load Scene"

			if self.param == "setpos" or self.param == "move" or self.param == "applyforce":
				self.xlabel = ctk.CTkLabel(self.frame, text="X:",font=("",18))
				self.xlabel.place(x=150,y=3.5)
				self.displayed_objects.append(self.xlabel)
				self.xentry = ctk.CTkEntry(self.frame)
				self.xentry.insert(0, self.args[0])
				self.xentry.place(x=175,y=2,relwidth=0.1,relheight=0.9)
				self.displayed_objects.append(self.xentry)
				self.ylabel = ctk.CTkLabel(self.frame, text="Y:",font=("",18))
				self.ylabel.place(x=230,y=3.5)
				self.displayed_objects.append(self.ylabel)
				self.yentry = ctk.CTkEntry(self.frame)
				self.yentry.insert(0, self.args[1])
				self.yentry.place(x=255,y=2,relwidth=0.1,relheight=0.9)
				self.displayed_objects.append(self.yentry)
			elif self.param == "setobjpos" or self.param == "moveobj":
				searched_object = scenetree.selected_name
				scene = scenetree.currentscene
				openfile = open("projects/"+project_name+"/Scenes/"+scene+".txt", "r")
				readfile = openfile.readlines()
				openfile.close()
				objecttemp = []
				for lines in readfile:
					value = lines.rstrip("\n")
					if value != "":
						objecttemp.append(value)
				self.optionmenu1 = ctk.CTkOptionMenu(self.frame, fg_color="#878787", button_color="#333333", values=objecttemp)
				self.optionmenu1.place(x=150, y=2.5, relwidth=0.2, relheight=0.8)
				self.optionmenu1.set(self.args[0])
				self.displayed_objects.append(self.optionmenu1)
				self.xlabel = ctk.CTkLabel(self.frame, text="X:", font=("", 18))
				self.xlabel.place(x=245, y=3.5)
				self.displayed_objects.append(self.xlabel)
				self.xentry = ctk.CTkEntry(self.frame)
				self.xentry.insert(0, self.args[1])
				self.xentry.place(x=270, y=2, relwidth=0.1, relheight=0.9)
				self.displayed_objects.append(self.xentry)
				self.ylabel = ctk.CTkLabel(self.frame, text="Y:", font=("", 18))
				self.ylabel.place(x=325, y=3.5)
				self.displayed_objects.append(self.ylabel)
				self.yentry = ctk.CTkEntry(self.frame)
				self.yentry.insert(0, self.args[2])
				self.yentry.place(x=350, y=2, relwidth=0.1, relheight=0.9)
				self.displayed_objects.append(self.yentry)
			elif self.param == "loadscene":
				openfile = open("projects/"+project_name+"/scenes.txt", "r")
				readfile = openfile.readlines()
				openfile.close()
				objecttemp = []
				for lines in readfile:
					value = lines.rstrip("\n")
					if value != "":
						objecttemp.append(value)
				self.optionmenu1 = ctk.CTkOptionMenu(self.frame, fg_color="#878787", button_color="#333333", values=objecttemp)
				self.optionmenu1.place(x=150, y=2.5, relwidth=0.4, relheight=0.8)
				self.optionmenu1.set(self.args[0])
				self.displayed_objects.append(self.optionmenu1)




			self.label = ctk.CTkLabel(self.frame, text=evtype,font=("",19))
			if self.param == "setobjpos":
				self.label.place(x=-10,y=2,relwidth=0.375,relheight=0.8)
			else:
				self.label.place(x=-20,y=2,relwidth=0.375,relheight=0.8)
			self.displayed_objects.append(self.label)

			self.del_button = ctk.CTkButton(self.frame, fg_color="#ff4040",text="X", font=("",19),command=self.delete_action)
			self.del_button.place(x=395,y=1,relwidth=0.08,relheight=0.9)
			self.displayed_objects.append(self.del_button)

	def load_system():
		event_system_canvas.delete('all')
		shown_widgets.clear()
		searched_object = scenetree.selected_name
		scene = scenetree.currentscene
		openfile = openfile = open("projects/"+project_name+"/Scenes/"+scene+"/"+searched_object+".es", "r")
		readfile = openfile.readlines()
		openfile.close()
		objecttemp = []
		for lines in readfile:
			value = lines.rstrip("\n")
			if value != "":
				objecttemp.append(value)
		lfp = 35
		eventindex = 0
		actionindex = 0
		lastevent = 0
		for i in objecttemp:
			initial = i.split("+")
			if initial[0] == "event":
				args = []
				if len(initial) == 3:
					args.append(initial[2])
				elif len(initial) == 4:
					args.append(initial[2])
					args.append(initial[3])
				temp = Event_OR_Action("event",initial[1],args,eventindex,actionindex,lfp,load_system)
				shown_widgets.append(temp)
				lastevent = eventindex
				eventindex += 1
				lfp += 70
				actionindex = 0
			elif initial[0] == "action":
				args = []
				if len(initial) == 3:
					args.append(initial[2])
				elif len(initial) == 4:
					args.append(initial[2])
					args.append(initial[3])
				elif len(initial) == 5:
					args.append(initial[2])
					args.append(initial[3])
					args.append(initial[4])
				temp = Event_OR_Action("action",initial[1],args,lastevent,actionindex,lfp,load_system)
				shown_widgets.append(temp)
				lfp += 70
				actionindex += 1
			event_system_canvas.configure(scrollregion=event_system_canvas.bbox("all"))




	def add_event(searched_type=""):
		if searched_type != "":
			searched_object = scenetree.selected_name
			scene = scenetree.currentscene
			openfile = open("projects/"+project_name+"/Scenes/"+scene+"/"+searched_object+".es", "r")
			readfile = openfile.readlines()
			openfile.close()
			objecttemp = []
			for lines in readfile:
				value = lines.rstrip("\n")
				if value != "":
					objecttemp.append(value)
			if searched_type == "keypress":
				objecttemp.append("event+keypress+Space")
			elif searched_type == "keyhold":
				objecttemp.append("event+keyhold+Space")
			elif searched_type == "colwith":
				objecttemp.append("event+colwith+"+searched_object)
			elif searched_type == "colbtw":
				objecttemp.append("event+colbtw+"+searched_object+"+"+searched_object)
			writefile = open("projects/"+project_name+"/Scenes/"+scene+"/"+searched_object+".es", "w")
			for i in objecttemp:
				writefile.writelines(i+"\n")
			writefile.close()
			load_system()
			

	def add_menu(event):
		addeventmenu.post(addeventbutton.winfo_rootx(), addeventbutton.winfo_rooty() + addeventbutton.winfo_height())

	def apply():
		searched_object = scenetree.selected_name
		scene = scenetree.currentscene
		temp = []
		for widget in shown_widgets:
			temp.append(widget.get())
		writefile = open("projects/"+project_name+"/Scenes/"+scene+"/"+searched_object+".es", "w")
		for lines in temp:
			writefile.writelines(lines+"\n")
		writefile.close()
		load_system()

	addeventbutton = ctk.CTkButton(root, text="Add Event", fg_color="#5f9467", font=("",20))
	addeventbutton.pack()
	addeventbutton.place(x=5,y=5,relwidth=0.3,relheight=0.1)
	addeventbutton.bind("<Button-1>", add_menu)

	addeventmenu = tk.Menu(root, tearoff=0)
	addeventmenu.add_separator()
	addeventmenu.add_command(label="Keypress",font=("",15),command=lambda: add_event("keypress"))
	addeventmenu.add_separator()
	addeventmenu.add_command(label="Keyhold",font=("",15),command=lambda: add_event("keyhold"))
	addeventmenu.add_separator()
	addeventmenu.add_command(label="Collision with",font=("",15),command=lambda: add_event("colwith"))
	addeventmenu.add_separator()
	addeventmenu.add_command(label="Collision between",font=("",15),command=lambda: add_event("colbtw"))

	apply_button = ctk.CTkButton(root, text="Apply", fg_color="#5f9467", font=("",20), command=apply)
	apply_button.place(x=449,y=5,relwidth=0.15,relheight=0.1)

	load_system()
	root.mainloop()



event_system_button = ctk.CTkButton(viewport_canvas,text="Event System",corner_radius=0, fg_color="#5f6670", font=("",20),command=EventSystemWindow)
event_system_button.place(x=0,y=0,relwidth=0.2,relheight=0.1)

def AttributesWindow():
	if scenetree.selected_name == "Camera2D":
		messagebox.showwarning("Warning", "Camera2D cant have Attributes")
		return True

	root = ctk.CTk()
	root.geometry("800x600")
	root.title("Attributes")
	if plattform == "win":
		root.iconbitmap("src/icon.ico")

	settingsframe = ctk.CTkFrame(root, width=250,height=380)
	settingsframe.place(x=260,y=10)

	settings = ctk.CTkLabel(settingsframe, text="Settings", font=("",30))
	settings.place(x=0,y=5,relwidth=0.5,relheight=0.1)

	apply_button = ctk.CTkButton(settingsframe, text="Apply", fg_color="#5f9467", font=("",20))
	apply_button.pack()
	apply_button.place(x=160,y=5,relwidth=0.3,relheight=0.1)

	class Attributes:
		def __init__(self):
			self.displayed_objects = []
			self.displayed_settings = []
			self.last = 60
			self.selected = None
			self.button_map = {}
			self.indexmap = {}
			self.checkvar = ctk.StringVar(value="off")
		def update(self):
			self.last = 60

			self.object = scenetree.selected_name
			self.scene = scenetree.currentscene

			#open the files
			openfile = open("projects/"+project_name+"/Scenes/"+self.scene+"/"+self.object+".config", "r")
			readfile = openfile.readlines()
			openfile.close()
			self.objecttemp = []
			for lines in readfile:
				self.objecttemp.append(lines.rstrip("\n"))

			#clear for update
			for objects in self.displayed_objects:
				objects.destroy()
			self.displayed_objects.clear()
			self.button_map.clear()
			self.indexmap.clear()

			index = 0

			if self.objecttemp[8] != "none":
				value = self.objecttemp[8]
				table = value.split(",")
				button = ctk.CTkButton(root, text="PhysicsObject",font=("",20),fg_color="#353536")
				button.configure(command=lambda button=button: self.select(button))
				button.bind("<Button-3>", lambda event, button=button: self.show_delete_option(button))
				button.place(x=20,y=self.last,relwidth=0.4,relheight=0.15)
				self.displayed_objects.append(button)
				self.last += 70
				self.button_map[button] = "PhysicsObject"
				self.indexmap[button] = index
				index += 1

			if self.objecttemp[10] != "none":
				value = self.objecttemp[10]
				button = ctk.CTkButton(root, text="Gravity",font=("",20),fg_color="#353536")
				button.configure(command=lambda button=button: self.select(button))
				button.bind("<Button-3>", lambda event, button=button: self.show_delete_option(button))
				button.place(x=20,y=self.last,relwidth=0.4,relheight=0.15)
				self.displayed_objects.append(button)
				self.last += 70
				self.button_map[button] = "Gravity"
				self.indexmap[button] = index
				index += 1
		def select(self, object1=None):
			if self.selected:
				self.selected.configure(fg_color="#353536")
			self.selected = object1
			self.selection()
			self.settings()

		def selection(self):
			self.displayed_objects[self.displayed_objects.index(self.selected)].configure(fg_color="#a1a1a1")

		def show_delete_option(self, button):
			delete_menu = tk.Menu(root, tearoff=0)
			delete_menu.add_command(label="Delete", font=("", 15), command=lambda: self.delete_attribute(button))
			delete_menu.post(root.winfo_pointerx(), root.winfo_pointery())

		def delete_attribute(self, button):
			type1 = self.button_map[button]
			if type1 == "PhysicsObject":
				self.objecttemp[8] = "none"
			if type1 == "Gravity":
				self.objecttemp[10] = "none"
			writefile = open("projects/"+project_name+"/Scenes/"+self.scene+"/"+self.object+".config", "w")
			for lines in self.objecttemp:
				writefile.writelines(lines+"\n")
			writefile.close()
			self.update()
			if self.displayed_objects != []:
				self.selected = attributes.displayed_objects[0]
				self.selection()
			self.settings()



		def settings(self):
			openfile = open("projects/"+project_name+"/Scenes/"+self.scene+"/"+self.object+".config", "r")
			readfile = openfile.readlines()
			openfile.close()
			self.objecttemp = []
			for lines in readfile:
				self.objecttemp.append(lines.rstrip("\n"))

			for objs in self.displayed_settings:
				objs.destroy()
			self.displayed_settings.clear()

			try:
				sel_name = self.button_map[self.selected]
				if sel_name == "PhysicsObject":
					list1 = self.objecttemp[8].split(",")
					static = ctk.CTkLabel(settingsframe, text="Static:",font=("",19))
					static.place(x=20,y=50,relwidth=0.2,relheight=0.1)
					self.displayed_settings.append(static)

					static_check = ctk.CTkCheckBox(settingsframe, text="CTkCheckBox", variable=self.checkvar, onvalue="on", offvalue="off")
					static_check.place(x=80,y=50,relwidth=0.1,relheight=0.1)
					if list1[0] == "True":
						self.checkvar.set("on")
					elif list1[0] == "False":
						self.checkvar.set("off")
					self.displayed_settings.append(static_check)

					mass = ctk.CTkLabel(settingsframe, text="Mass:",font=("",19))
					mass.place(x=20,y=90,relwidth=0.2,relheight=0.1)
					self.displayed_settings.append(mass)

					mass_entry = ctk.CTkEntry(settingsframe)
					mass_entry.place(x=80,y=95,relwidth=0.3,relheight=0.075)
					mass_entry.insert(0, list1[1])
					self.displayed_settings.append(mass_entry)

					inertia = ctk.CTkLabel(settingsframe, text="Inertia:",font=("",19))
					inertia.place(x=17.5,y=130,relwidth=0.25,relheight=0.1)
					self.displayed_settings.append(inertia)

					inertia_entry = ctk.CTkEntry(settingsframe)
					inertia_entry.place(x=80,y=135,relwidth=0.3,relheight=0.075)
					inertia_entry.insert(0, list1[2])
					self.displayed_settings.append(inertia_entry)
				if sel_name == "Gravity":
					mass = ctk.CTkLabel(settingsframe, text="Mass:",font=("",19))
					mass.place(x=20,y=50,relwidth=0.2,relheight=0.1)
					self.displayed_settings.append(mass)

					mass_entry = ctk.CTkEntry(settingsframe)
					mass_entry.place(x=80,y=55,relwidth=0.3,relheight=0.075)
					mass_entry.insert(0, self.objecttemp[10])
					self.displayed_settings.append(mass_entry)
			except:
				pass
		def apply(self): #5
			sel_name = self.button_map[self.selected]
			if sel_name == "PhysicsObject":
				if re.match(r'^\d+$', self.displayed_settings[3].get()):
					if re.match(r'^\d+$', self.displayed_settings[5].get()):
						bool1 = "False"
						if self.checkvar.get() == "on":
							bool1 = "True"
						elif self.checkvar.get() == "off":
							bool1 = "False"
						self.objecttemp[8] = bool1+","+self.displayed_settings[3].get()+","+self.displayed_settings[5].get()
						writefile = open("projects/"+project_name+"/Scenes/"+self.scene+"/"+self.object+".config", "w")
						for lines in self.objecttemp:
							writefile.writelines(lines+"\n")
						writefile.close()
						if attributes.displayed_objects != []:
							self.selection()
							self.settings()
					else:
						messagebox.showwarning("Warning", "Inertia value not valid")
						if attributes.displayed_objects != []:
							self.selection()
							self.settings()
				else:
					messagebox.showwarning("Warning", "Mass value not valid")
					if attributes.displayed_objects != []:
							self.selection()
							self.settings()
			if sel_name == "Gravity":
				if re.match(r'^\d+$', self.displayed_settings[1].get()):
					self.objecttemp[10] = self.displayed_settings[1].get()
					writefile = open("projects/"+project_name+"/Scenes/"+self.scene+"/"+self.object+".config", "w")
					for lines in self.objecttemp:
						writefile.writelines(lines+"\n")
					writefile.close()
					if attributes.displayed_objects != []:
						self.selection()
						self.settings()
				else:
					messagebox.showwarning("Warning", "Mass value not valid")
					if attributes.displayed_objects != []:
							self.selection()
							self.settings()



	attributes = Attributes()
	attributes.update()
	if attributes.displayed_objects != []:
		attributes.selected = attributes.displayed_objects[0]
		attributes.selection()
		attributes.settings()

	apply_button.configure(command=attributes.apply)

	def add_attribute(type1=""):
		object1 = scenetree.selected_name
		scene = scenetree.currentscene
		#open the files
		openfile = open("projects/"+project_name+"/Scenes/"+scene+"/"+object1+".config", "r")
		readfile = openfile.readlines()
		openfile.close()
		objecttemp = []
		for lines in readfile:
			objecttemp.append(lines.rstrip("\n"))
		if type1 == "PhysicsObject":
			if objecttemp[8] != "none":
				messagebox.showwarning("Warning", "Object already has Attribute PhysicsObject")
			else:
				objecttemp[8] = "False,1,100"
				writefile = open("projects/"+project_name+"/Scenes/"+scene+"/"+object1+".config", "w")
				for lines in objecttemp:
					writefile.writelines(lines+"\n")
				writefile.close()
		if type1 == "Gravity":
			if objecttemp[10] != "none":
				messagebox.showwarning("Warning", "Object already has Attribute Gravity")
			else:
				objecttemp[10] = "1"
				writefile = open("projects/"+project_name+"/Scenes/"+scene+"/"+object1+".config", "w")
				for lines in objecttemp:
					writefile.writelines(lines+"\n")
				writefile.close()
		attributes.update()
		if attributes.displayed_objects != []:
			attributes.selected = attributes.displayed_objects[0]
			attributes.selection()
			attributes.settings()


	def add_menu(event):
		addattributemenu.post(addattributebutton.winfo_rootx(), addattributebutton.winfo_rooty() + addattributebutton.winfo_height())

	addattributebutton = ctk.CTkButton(root, text="+", fg_color="#5f9467", font=("",20))
	addattributebutton.pack()
	addattributebutton.place(x=5,y=5,relwidth=0.1,relheight=0.1)
	addattributebutton.bind("<Button-1>", add_menu)

	addattributemenu = tk.Menu(root, tearoff=0)
	#addattributemenu.add_command(label="Gravity",font=("",15),command=lambda: add_attribute("Gravity"))
	addattributemenu.add_command(label="Physics Object",font=("",15),command=lambda: add_attribute("PhysicsObject"))
	#addattributemenu.add_command(label="Camera Follow",font=("",15),command=lambda: add_attribute("camerafollow"))



	root.mainloop()



properties_panel.scenetreelink = scenetree
attributes_button = ctk.CTkButton(viewport_canvas,text="Attributes",corner_radius=0, fg_color="#5f6670", font=("",20),command=AttributesWindow)
attributes_button.place(x=150,y=0,relwidth=0.2,relheight=0.1)

def on_left_button_release(event):
	if scenetree.selected_name != "Camera2D":
		if fm.dragged == True and properties_panel.inframe() == True:
			openfile = open("projects/"+project_name+"/Scenes/"+scenetree.currentscene+"/"+scenetree.selected_name+".config","r")
			readfile = openfile.readlines()
			openfile.close()
			objecttemp = []
			for lines in readfile:
				objecttemp.append(lines.rstrip("\n"))
			objecttemp[6] = fm.button_file_map[fm.dragged_button]

			writefile = open("projects/"+project_name+"/Scenes/"+scenetree.currentscene+"/"+scenetree.selected_name+".config","w")
			for lines in objecttemp:
				writefile.writelines(lines+"\n")
			writefile.close()

			properties_panel.update()


app.bind("<ButtonRelease-1>", on_left_button_release)

def new_scene():
	dialog = ctk.CTkInputDialog(text="Scene Name:", title="New Scene")
	value = dialog.get_input()
	if value != "":
		openfile = open("projects/"+project_name+"/scenes.txt", "r")
		readfile = openfile.readlines()
		openfile.close()
		objecttemp = []
		for lines in readfile:
			objecttemp.append(lines.rstrip("\n"))
		objecttemp.append(value)
		writefile = open("projects/"+project_name+"/scenes.txt", "w")
		currentindex = 0
		for lines in objecttemp:
			if currentindex != (len(objecttemp)-1):
				writefile.writelines(lines+"\n")
			else:
				writefile.writelines(lines)
		writefile.close()

		with open("projects/"+project_name+"/Scenes/"+value+".txt", "w") as f:
			f.write("")

		directory_path = "projects/"+project_name+"/Scenes/"+value
		os.makedirs(directory_path, exist_ok=True)

		cameraconfig = ["#TRANSFORM","0","0","#BGCOLOR","#ffffff"]
		with open(directory_path+"/Camera2D.config", "w") as f:
			for lines in cameraconfig:
				f.write(lines+"\n")

		fm.update()




		


#adding a file menu into menubar
file_menu = tk.Menu(menu_bar, tearoff=False, font=menu_font)
file_menu.add_command(label="New Scene", command=new_scene)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_separator()
file_menu.add_command(label="Project Manager", command=openprcmanager)
file_menu.add_command(label="Quit", command=app.quit)

def opendocs():
	script_dir = os.path.dirname(os.path.realpath(__file__))
	subprocess.Popen('cmd /c cd /d "{}" &'.format(script_dir), shell=True)
	subprocess.Popen('python opendocs.py', shell=True)

#adding a edit menu into menubar
edit_menu = tk.Menu(menu_bar, tearoff=False, font=menu_font)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Open Documentation", command=opendocs)


def export():
	def copy_files(source_dir, destination_dir):
		file_list = os.listdir(source_dir)
		for file_name in file_list:
			source_path = os.path.join(source_dir, file_name)
			destination_path = os.path.join(destination_dir, file_name)
			shutil.copy2(source_path, destination_path)

	try:
		os.remove("projects/"+project_name+"/build")
	except:
		pass
	directory_path = "projects/"+project_name+"/build"
	os.makedirs(directory_path, exist_ok=True)

	directory_path = "projects/"+project_name+"/build/src"
	os.makedirs(directory_path, exist_ok=True)

	copy_files("projects/"+project_name+"/Files", "projects/"+project_name+"/build/src")
	shutil.copy2("Engine.py", "projects/"+project_name+"/build")

	exporter = Export(project_name)
	exporter.build()

	relative_path = "projects/"+project_name+"/build/main.py"
	absolute_path = os.path.abspath(relative_path)
	file_dir = os.path.dirname(absolute_path)

	try:
		directory_path = filedialog.askdirectory(mustexist=True)
		if directory_path:
			destination_path = os.path.join(directory_path, "build")
			shutil.rmtree(destination_path, ignore_errors=True)  # Remove the existing "build" directory if it exists
			shutil.copytree("projects/" + project_name + "/build", destination_path)
	except Exception as e:
		print("An error occurred:", str(e))




#adding a selection menu into menubar
export_menu = tk.Menu(menu_bar, tearoff=False, font=menu_font)
menu_bar.add_cascade(label="Export", menu=export_menu)
export_menu.add_command(label="To File", command=export)



properties_apply_button = ctk.CTkButton(properties_panel_heading, text="Apply", fg_color="#5f9467", font=("",20), command=properties_panel.apply)
properties_apply_button.pack()
properties_apply_button.place(x=170,y=5,relwidth=0.3)


general_update("startup")
scenetree.select(scenetree.displayed_objects[0])
viewport.update()

app.mainloop()

print("press enter to quit> ")