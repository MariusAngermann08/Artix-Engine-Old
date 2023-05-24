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

openfile = open("prcopen.info", "r")
readfile = openfile.readlines()
project_name = readfile[0]
openfile.close()


def import_file():
	filename = filedialog.askopenfilename(initialdir=os.path.expanduser("~/Documents"), title="Import File", filetypes=(("png files","*.png"),("jpeg files","*.jpg")))





#default costumtkinter setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
ctk.set_widget_scaling(1.5)  
app = ctk.CTk()
app.geometry("1920x1080")
app.after(0, lambda:app.state('zoomed'))
app.title("Artisan Studio - Project:>" + project_name)

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
file_manager_frame = ctk.CTkFrame(app,750,230,border_width=0,fg_color="#172a38",border_color="#000000")
file_manager_frame.pack()
file_manager_frame.place(x=270,y=430)

file_manager_heading = ctk.CTkFrame(app,750,30,border_width=0,fg_color="#2b2b2b",border_color="#000000")
file_manager_heading.pack()
file_manager_heading.place(x=270,y=430)

file_manager_label = ctk.CTkLabel(file_manager_heading, text="File Manager", fg_color="transparent")
file_manager_label.pack()
file_manager_label.place(relwidth=1,relheight=1)
file_manager_label.lift()

file_manager_button = ctk.CTkButton(file_manager_heading, text="Import", command=import_file)
file_manager_button.pack()
file_manager_button.place(relwidth=0.2,relheight=1)

#filetest
testimg = ctk.CTkImage(dark_image=Image.open("src/icons/image_icon.png"),size=(50,60))
button = ctk.CTkButton(file_manager_frame, text="", image=testimg, width=50, height=60)
button.pack()
button.place(x=10,y=40,relwidth=0.1,relheight=0.3)
name_label = ctk.CTkLabel(file_manager_frame, text="texture.png", fg_color="transparent")
name_label.pack()
name_label.place(x=2,y=110,relwidth=0.12,relheight=0.07)








app.mainloop()

print("press enter to quit> ")