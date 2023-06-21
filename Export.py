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
			self.exportfile.append(self.scenes[currentindex]+" = engine.Scene(\""+self.scenes[currentindex]+"\", 60, engine.screen)\n")
			for objs in self.objects[currentindex]:
				#read the config
				openfile = open("projects/"+self.project_name+"/Scenes/"+self.scenes[currentindex]+"/"+objs+".config", "r")
				readfile = openfile.readlines()
				openfile.close()

				objecttemp = []
				for lines in readfile:
					objecttemp.append(lines.rstrip("\n"))

				value = objs+" = "+self.scenes[currentindex]+".GameObject(\""+objs+"\", \"Sprite\", False)\n"
				self.exportfile.append(value)

				if objecttemp[6] != "none":
					value = objs+".add_property(\"texture\", \"src/"+objecttemp[6]+"\")\n"
					self.exportfile.append(value)
				

				scalex = int(objecttemp[3])
				scaley = int(objecttemp[4])
				posx = int(float(objecttemp[1]))
				posy = int(float(objecttemp[2]))

				canvaswidth = 1100
				canvasheight = 630
				windowwidth = 800
				windowheight = 600

				xfactor = windowwidth / canvaswidth
				yfactor = windowheight / canvasheight

				fscalex = scalex * xfactor
				fscaley = scaley * yfactor
				fposx = posx * xfactor - fscalex / 2
				fposy = posy * yfactor
				

				value = objs+".transform.scale.x = "+str(fscalex)+"\n"
				self.exportfile.append(value)
				value = objs+".transform.scale.y = "+str(fscaley)+"\n"
				self.exportfile.append(value)
				value = objs+".transform.position.x = "+str(fposx)+"\n"
				self.exportfile.append(value)
				value = objs+".transform.position.y = "+str(fposy)+"\n"
				self.exportfile.append(value)
				value = self.scenes[currentindex]+".game_objects.append("+objs+")\n"
				self.exportfile.append(value)

				if objecttemp[8] != "none":
					single = objecttemp[8].split(",")
					print(objecttemp[8])
					print(single)
					static = "False"
					if single[0] == "True":
						static = "True"
					else:
						static = "False"
					mass = single[1]
					inertia = single[2]
					value = objs+".attributes.attributes.append("+objs+".attributes.PhysicsObject(position=("+str(fposx)+","+str(fposy)+"),static="+static+",own_size=("+str(fscalex* 1.6)+","+str(fscaley)+"), space_path="+self.scenes[currentindex]+".space, mass="+mass+",inertia="+inertia+"))\n"
					self.exportfile.append(value)
					value = objs+".attributes.attribute_names.append(\"PhysicsObject\")\n"
					self.exportfile.append(value)




				self.exportfile.append("\n")
			currentindex += 1



		self.exportfile.append("while True:\n")
		self.exportfile.append("	events = []\n")
		self.exportfile.append("	for event in pygame.event.get():\n")
		self.exportfile.append("		if event.type == pygame.QUIT:\n")
		self.exportfile.append("			pygame.quit()\n")
		self.exportfile.append("			sys.exit()\n")
		self.exportfile.append("		if event.type == pygame.KEYDOWN:\n")
		self.exportfile.append("			events.append(event)\n")
		self.exportfile.append("	DefaultScene.render(events)\n")
		#self.exportfile.append("\n")
		#self.exportfile.append("\n")
		#self.exportfile.append("\n")


		#creating the exported file
		writefile = open("projects/"+self.project_name+"/build/main.py", "w")
		for lines in self.exportfile:
			writefile.writelines(lines)
		writefile.close()
