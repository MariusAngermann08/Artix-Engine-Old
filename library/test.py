from tkinter import *
import customtkinter as ctk
import sys
import os
import shutil
import subprocess

plattform = ""
if sys.platform.startswith('win'):
	plattform = "win"

root = ctk.CTk()
root.geometry("1000x700")
root.title("Attributes")
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
ctk.set_widget_scaling(1.5)
if plattform == "win":
	root.iconbitmap("src/icon.ico")

recentlabel = ctk.CTkLabel(root,text="Recent Projects:",font=("",30))
recentlabel.place(x=5,y=50)
projects_canvas = ctk.CTkCanvas(root, width=995,height=560,bg="#242424")
projects_canvas.place(x=0,y=130)
cscrollbar = ctk.CTkScrollbar(root, command=projects_canvas.yview)
cscrollbar.place(relx=1, rely=0.175, relheight=0.82, anchor='ne')
projects_canvas.configure(yscrollcommand=cscrollbar.set)

def on_canvas_mousewheel(event):
	projects_canvas.yview_scroll(-1 * int(event.delta/120), "units")

projects_canvas.bind_all("<MouseWheel>", on_canvas_mousewheel)

class Project:
	def __init__(self, name="", pos=[10,10]):
		self.name = name
		self.frame = ctk.CTkFrame(projects_canvas,fg_color="#363636")
		self.frame.place(x=pos[0],y=pos[1],relwidth=0.8,relheight=0.2)
		self.label = ctk.CTkLabel(self.frame, text=self.name,font=("",27))
		self.label.place(x=10,y=10)
	def kill(self):
		self.frame.destroy()



test = Project("DemoProject", pos=[10,10])

create_button = ctk.CTkButton(root, text="Create Project", font=("",20))
create_button.place(x=0,y=0,relwidth=0.25,relheight=0.1)

def update():
	projects_canvas.configure(scrollregion=projects_canvas.bbox("all"))

update()

root.mainloop()