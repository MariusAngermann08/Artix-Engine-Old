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
import os
import customtkinter as ctk
from PIL import Image
import shutil
import subprocess
import sys

openfile = open("prcopen.info", "r")
readfile = openfile.readlines()
project_name = readfile[0]
openfile.close()

scenes = []








#default costumtkinter setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
ctk.set_widget_scaling(1.5)  
app = ctk.CTk()
app.geometry("1920x1080")
app.after(0, lambda:app.state('zoomed'))
app.title("Artix Engine - Project:>" + project_name)
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

#adding a file menu into menubar
file_menu = tk.Menu(menu_bar, tearoff=False, font=menu_font)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New Scene")
file_menu.add_command(label="Save")
file_menu.add_command(label="Save as")
file_menu.add_command(label="Project Settings")
file_menu.add_separator()
file_menu.add_command(label="Project Manager", command=openprcmanager)
file_menu.add_command(label="Quit", command=app.quit)

#adding a edit menu into menubar
edit_menu = tk.Menu(menu_bar, tearoff=False, font=menu_font)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Copy")
edit_menu.add_command(label="Paste")
edit_menu.add_command(label="Undo")
edit_menu.add_command(label="Redo")
edit_menu.add_command(label="Editor Settings")

#adding a selection menu into menubar
selection_menu = tk.Menu(menu_bar, tearoff=False, font=menu_font)
menu_bar.add_cascade(label="Selection", menu=selection_menu)
selection_menu.add_command(label="Select all")
selection_menu.add_command(label="Clear Selection")

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


class FileManager:
	def __init__(self):
		self.menu = tk.Menu(app, tearoff=0)
		self.menu.add_command(label="Delete", command=self.delete_file, font=("",15))
		self.displayed_files = []
		self.files_list = []
		self.button_file_map = {}
		self.FileLoader()

	def FileLoader(self):
		self.files_list.clear()
		openfile = open("projects/"+project_name+"/files.txt", "r")
		readfile = openfile.readlines()
		for lines in readfile:
			line = lines.rstrip("\n")
			self.files_list.append(line)

	def display_files(self):
		currentindex = 0
		self.displayed_files = []
		lastbuttonpos = []
		lastlabelpos = []
		attempts = 0
		numberinline = 0
		newline = False
		for lines in self.files_list:
			testimg = ctk.CTkImage(dark_image=Image.open("src/icons/image_icon.png"),size=(50,60))
			button = ctk.CTkButton(file_manager_frame, text="", image=testimg, width=50, height=60)
			button.bind("<Button-3>", self.open_menu)
			name_label = ctk.CTkLabel(file_manager_frame, text=lines, fg_color="transparent")
			self.button_file_map[button] = lines
			self.displayed_files.append(testimg)
			self.displayed_files.append(button)
			self.displayed_files.append(name_label)
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
		self.displayed_files.clear()
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
		print("deleted file "+file_name)
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

	

fm = FileManager()
fm.display_files()
fm.update()





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





file_manager_button = ctk.CTkButton(file_manager_heading, text="Import", command=import_file)
file_manager_button.pack()
file_manager_button.place(relwidth=0.2,relheight=1)




def AttributesWindow():
	root = ctk.CTk()
	root.geometry("800x600")
	root.title("Attributes")
	root.iconbitmap("src/icon.ico")
	root.mainloop()

def EventSystemWindow():
	root = ctk.CTk()
	root.geometry("800x600")
	root.title("Event System")
	root.iconbitmap("src/icon.ico")
	root.mainloop()



viewport = ctk.CTkCanvas(app,width=1100,height=630)
viewport.pack()
viewport.place(x=415,y=5)

event_system_button = ctk.CTkButton(viewport,text="Event System",corner_radius=0, fg_color="#5f6670", font=("",20),command=EventSystemWindow)
event_system_button.pack()
event_system_button.place(x=0,y=0,relwidth=0.2,relheight=0.1)

attributes_button = ctk.CTkButton(viewport,text="Attributes",corner_radius=0, fg_color="#5f6670", font=("",20),command=AttributesWindow)
attributes_button.pack()
attributes_button.place(x=150,y=0,relwidth=0.2,relheight=0.1)

viewporttools = ctk.CTkSegmentedButton(viewport,values=["Move","Scale","Rotate"])
viewporttools.pack()
viewporttools.place(x=0,y=45)

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


addbutton = ctk.CTkButton(scenetreeheading, text="+", fg_color="#5f9467", font=("",20))
addbutton.pack()
addbutton.place(x=5,y=5,relwidth=0.2,relheight=0.7)


class SceneTree:
	def __init__(self,link=[]):
		self.sceneslink = link
		self.currentscene = []
		self.displayed_objects = []
	def load_scene(self, name=""):
		search = 0
		currentscene = name
		for each in self.sceneslink:
			if each.name == name:
				search = self.sceneslink.index(each)
				break
		scenenamelabel.configure(text=self.sceneslink[search].name)
		currentindex = 0
		lastpos = [25, 70]
		for each in self.sceneslink[search].objects:
			if each.type == "Camera2D":
				button = ctk.CTkButton(scenetreecanvas, text=each.type, font=("", 15), fg_color="#252626")
			else:
				button = ctk.CTkButton(scenetreecanvas, text=each.name, font=("", 15), fg_color="#252626")

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




	def update(self):
		self.sceneslink = scenes
		for objects in self.displayed_objects:
			objects.destroy()
		self.displayed_objects.clear()
		self.load_scene(self.currentscene)

		

scenetree = SceneTree(link=scenes)


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



defaultscene = Scene("Example Scene", link=scenes)
scenes.append(defaultscene)

scenetree.load_scene("Example Scene")

defaultscene.add_object(type="Sprite2D", name="testobj")
defaultscene.add_object(type="Sprite2D", name="coll")
defaultscene.add_object(type="Sprite2D", name="bird")
defaultscene.add_object(type="Sprite2D", name="obj1")
defaultscene.add_object(type="Sprite2D", name="3dModel")
defaultscene.add_object(type="Sprite2D", name="another one")
defaultscene.add_object(type="Sprite2D", name="3dCow")
defaultscene.add_object(type="Sprite2D", name="another")







app.mainloop()

print("press enter to quit> ")