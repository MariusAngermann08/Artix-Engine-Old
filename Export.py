class Export:
	def __init__(self, project_name=""):
		self.project_name = project_name
		self.scenes = []
		self.objects = []
		self.exportfile = []
	def build(self):
		#open the scenes file
		openfile = open("projects/"+self.project_name+"/scenes.txt", "r")
		readfile = openfile.readlines()
		openfile.close()
		for lines in readfile:
			if lines.rstrip("\n") != "":
				self.scenes.append(lines.rstrip("\n"))

		#open the objects file of scene
		openfile = open("projects/"+self.project_name+"/Scenes/"+self.scenes[0]+".txt", "r")
		readfile = openfile.readlines()
		openfile.close()
		temp = []
		for lines in readfile:
			if lines.rstrip("\n") != "":
				temp.append(lines.rstrip("\n"))
		self.objects.append(temp)
		temp.clear()

		#write the file
		self.exportfile.append("import pygame\n")
		self.exportfile.append("import pymunk\n")
		self.exportfile.append("import sys\n")
		self.exportfile.append("import math\n")
		self.exportfile.append("from collections import namedtuple\n")
		self.exportfile.append("\n")
		self.exportfile.append("from Engine import Engine")
		self.exportfile.append("\n")
		self.exportfile.append("\n")
		
		self.exportfile.append("engine = Engine(\""+self.project_name+"\")\n")
		self.exportfile.append("engine.engine_config([800,600],\""+self.project_name+"\""+",60)\n")
		self.exportfile.append("\n")

		currentindex = 0
		for scenes in self.objects:
			self.exportfile.append(self.scenes[currentindex]+" = engine.Scene(\""+self.scenes[currentindex]+"\", 60, engine.screen)")
			for objs in scenes:
				pass
			currentindex += 1



		
		#self.exportfile.append("\n")
		#self.exportfile.append("\n")
		#self.exportfile.append("\n")
		#self.exportfile.append("\n")


		#creating the exported file
		writefile = open("library/build.py", "w")
		for lines in self.exportfile:
			writefile.writelines(lines)
		writefile.close()


build = Export("SuperCoolGame")
build.build()