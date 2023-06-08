# This is the Project manager it is made to create and manage your game project
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


import pygame
import sys
import os
import shutil
import subprocess

from ui_modules.ui_input import Input
from ui_modules.ui_button import Button
from ui_modules.ui_askbox import AskBox






pygame.init()

flag = pygame.NOFRAME

icon = pygame.image.load("src/icon.png")

pygame.display.set_icon(icon)

screen = pygame.display.set_mode((1000,700),flag)

clock = pygame.time.Clock()


rendered_projects = []
projects_initialized = []
last_pos = [0,0]

class rendered_project:
	default_font = pygame.font.SysFont(None,35)
	edit_font = pygame.font.SysFont("Agency FB",20)
	render_costumes = [
		pygame.image.load("src/colored_shapes/project_render.png"),
		pygame.image.load("src/colored_shapes/project_render_select.png")
	]
	delete_costumes = [
		pygame.image.load("src/icons/delete.png"),
		pygame.image.load("src/icons/delete_hover.png")
	]
	def __init__(self,project_name="default-project",last_opened_str="never",last_position=[0,0]):
		self.name = project_name
		self.last_edit = last_opened_str
		self.title = self.default_font.render(self.name,True,(255,255,255))
		self.edit_label = self.edit_font.render("LAST EDITED: " + self.last_edit,True,(255,255,255))
		self.selected = False
		self.delete_hovered = False

		if last_position == [0,0]:
			self.position = [10,200]
		else:
			self.position = [10,last_position[1]+200]

		self.del_pos = [self.position[0]+495,self.position[1]+55]
		self.open_button = Button("Open",pygame.font.SysFont(None,30),200,60,(self.position[0]+285,self.position[1]+60),(11, 37, 59),(5, 16, 26),(35, 57, 77),12)
	def render(self,display_surface):
		
		if self.selected == False:
			costume = self.render_costumes[0]
		else:
			costume = self.render_costumes[1]

		if self.delete_hovered == True:
			delete_costume = self.delete_costumes[1]
		else:
			delete_costume = self.delete_costumes[0]

		delete_costume = pygame.transform.scale(delete_costume, (60,60))

		test_hover = self.delete_costumes[0]
		test_hover = pygame.transform.scale(test_hover, (60,60))
		test_col = test_hover.get_rect()
		test_col = test_col.move(self.del_pos)

		if test_col.collidepoint(pygame.mouse.get_pos()):
			self.delete_hovered = True
		else:
			self.delete_hovered = False

		if self.open_button.check_click():
			opentemp = open("prcopen.info", "w")
			opentemp.writelines(self.name)
			opentemp.close()
			script_dir = os.path.dirname(os.path.realpath(__file__))
			subprocess.Popen('cmd /c cd /d "{}" &'.format(script_dir), shell=True)
			subprocess.Popen('python Editor.py', shell=True)
			pygame.quit()
			sys.exit()

		costume_scaled = pygame.transform.scale(costume, (600,170))
		display_surface.blit(costume_scaled, self.position)
		display_surface.blit(self.title, (50,self.position[1]+30))
		display_surface.blit(self.edit_label, (50,self.position[1]+80))
		self.open_button.draw(display_surface)
		display_surface.blit(delete_costume, (self.del_pos[0],self.del_pos[1]))
	def move_button(self, newvector=[0,0]):
		self.open_button.move(newvector)





def add_prc_to_render(last_pos):
	for prcs in projects_initialized:
		openfile = open('projects/'+prcs+'/project.artix', 'r')
		readfile = openfile.readlines()
		rendered_projects.append(rendered_project(prcs,str(readfile[0]),last_pos))
		last_pos = [10,last_pos[1]+200]
		openfile.close()

headbar = pygame.image.load("src/colored_shapes/headbar.png")
headbar_render = pygame.transform.scale(headbar, (1000,50))

title_font = pygame.font.SysFont(None,30)
window_title = title_font.render("Artix Project Manager",True,(255,255,255))

def initialize_projects():
	opened = open('registered_projects.info', 'r')
	read = opened.readlines()
	for lines in read:
		# rstrip() to get rid of new line character
		line = lines.rstrip()
		if line != "":
			projects_initialized.append(line)
	print(projects_initialized)
	opened.close()


def render_projects():
	for elements in rendered_projects:
		elements.render(screen)
	
	
def scroll_projects(status="down"):
	currentindex = 0
	if status == "down":
		for singleprcs in rendered_projects:
			singleprcs.position = [singleprcs.position[0],singleprcs.position[1]-30]
			singleprcs.del_pos = [singleprcs.del_pos[0],singleprcs.del_pos[1]-30]
			singleprcs.move_button([0,-30])
	elif status == "up":
		for singleprcs in rendered_projects:
			singleprcs.position = [singleprcs.position[0],singleprcs.position[1]+30]
			singleprcs.del_pos = [singleprcs.del_pos[0],singleprcs.del_pos[1]+30]
			singleprcs.move_button([0,30])

def del_prc(prc_name=""):
	with open('registered_projects.info', 'r') as file:
		file_contents = file.readlines()
		file_contents = [line for line in file_contents if prc_name not in line]
	with open('registered_projects.info', 'w') as file:
		file.writelines(file_contents)
	folder_path = "./projects/" + prc_name
	shutil.rmtree(folder_path)


	
	
	
	




exit_button_costumes = [
	pygame.image.load("src/icons/exit.png"),
	pygame.image.load("src/icons/exit_hover.png")
]

exit_button = exit_button_costumes[0]
exit_button_render = pygame.transform.scale(exit_button, (40,40))
exit_button_colshape = exit_button_render.get_rect()
exit_button_colshape.x = 945
exit_button_colshape.y = 5


font_1 = pygame.font.SysFont("OCR-A Extended",40)
recent_projects_label = font_1.render("Recent Projects:",True,(255,255,255))
new_project_button = Button("Create Project",pygame.font.SysFont(None,30),200,40,(30,70),(92, 91, 91),(56, 56, 56),(143, 141, 141),12)


renderit = True
final = ""
new_project_box = AskBox("Enter Project Name","New Project",(1000,700))

fade_rect = pygame.Rect(0,0,1000,200)

initialize_projects()
add_prc_to_render(last_pos)

while True:
	if exit_button_colshape.collidepoint(pygame.mouse.get_pos()):
		exit_button = exit_button_costumes[1]
		exit_button_render = pygame.transform.scale(exit_button, (40,40))
	else:
		exit_button = exit_button_costumes[0]
		exit_button_render = pygame.transform.scale(exit_button, (40,40))


	for event in pygame.event.get():
		new_project_box.input_box.get_input(event)

		if event.type == pygame.QUIT:
			print("")
			print("")
			print("press enter to quit >")
			pygame.quit()
			sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			if exit_button_colshape.collidepoint(event.pos):
				print("")
				print("")
				print("")
				print("Press enter to quit>")
				pygame.quit()
				sys.exit()

		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				for renderedobjects in rendered_projects:
					if renderedobjects.delete_hovered == True:
						del_prc(renderedobjects.name)
						rendered_projects = []
						projects_initialized = []
						initialize_projects()
						print(projects_initialized)
						add_prc_to_render(last_pos)
			if event.button == 4: # Scroll up
				if rendered_projects[0].position[1] <= 230:
					scroll_projects("up")
			elif event.button == 5: # Scroll down
				if rendered_projects[len(rendered_projects)-1].position[1] >= 500:
					scroll_projects("down")
			
					
	#logic
	if new_project_button.check_click() == True:
		renderit = False


	#rendering
	screen.fill((46, 44, 44))

	render_projects()
	pygame.draw.rect(screen,(46, 44, 44),fade_rect)
	screen.blit(headbar_render, (0,0))
	screen.blit(window_title, (370,15))
	screen.blit(exit_button_render, (945,5))


	screen.blit(recent_projects_label,(35,135))
	new_project_button.draw(screen)
	

	if renderit != True:
		renderit = new_project_box.get_active()
		if renderit != True:
			new_project_box.render(screen,(1000,700))
		else:
			registered_projects_temp = []
			fileopen = open('registered_projects.info','r')
			fileread = fileopen.readlines()
			for lines in fileread:
				registered_projects_temp.append(lines)
			fileopen.close()
			final = new_project_box.get_value()
			renderit = True
			fileopen_privat = open('registered_projects.info','w')
			fileopen_privat.writelines(final+'\n')

			current_dir = os.getcwd()
			projects_path = os.path.join(current_dir, "projects")
			new_folder_path = os.path.join(projects_path, final)
			os.mkdir(new_folder_path)
			file_path = os.path.join(new_folder_path, "project.artix")
			with open(file_path, 'w') as f:
				f.write('never')

			file_path = os.path.join(new_folder_path, "files.txt")
			with open(file_path, 'w') as f:
				f.write('')

			file_path = os.path.join(new_folder_path, "scenes.txt")
			with open(file_path, 'w') as f:
				f.write('DefaultScene')

			file_path = os.path.join(new_folder_path, "Scenes")
			os.mkdir(file_path)
			actualfile = os.path.join(file_path, "DefaultScene.txt")
			with open(actualfile, 'w') as f:
				f.write('')

			loe = len(registered_projects_temp)
			currentindex = 0
			for elements in registered_projects_temp:
				if currentindex == (loe-1):
					fileopen_privat.writelines(elements+'\n')
				else:
					fileopen_privat.writelines(elements)
				currentindex += 1
			fileopen_privat.close()
			final = ""
			rendered_projects = []
			projects_initialized = []
			initialize_projects()
			print(projects_initialized)
			add_prc_to_render(last_pos)
	

	pygame.display.update()
	clock.tick(60)

	if pygame.display.get_active() == False:
		pygame.quit()
		sys.exit()

print("")