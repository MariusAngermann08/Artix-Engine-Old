# This is the Engine module it is used to power the games made with the engine
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
import math
from collections import namedtuple
import pymunk

class Engine:
	def __init__(self,name):
		try:
			pygame.init()
			self.prc_name = name
			self.render_size = (600,300)
			self.render_caption = "default caption"
			self.screen = pygame.display.set_mode(self.render_size)
			self.frame_rate = 60
			self.clock = pygame.time.Clock()
			pygame.display.set_caption(self.render_caption)
			print("Engine initialized")
		except:
			print("Error Engine was not initialized")
	def engine_controller(self):
		pass
	def engine_config(self,window_size=[600,300],window_caption="default caption",new_frame_rate=60):
		self.render_size = (window_size[0],window_size[1])
		self.render_caption = window_caption
		self.frame_rate = new_frame_rate
		self.screen = pygame.display.set_mode(self.render_size)
		pygame.display.set_caption(self.render_caption)
	class Scene:
		game_objects = []
		rigid_bodies = []
		def __init__(self, scene_name="default scene", engine_frame_rate=60, display_surface=0, global_gravity=(0,500)):
			self.name = scene_name
			self.frame_rate = engine_frame_rate
			self.bg_color = (255,255,255)
			self.screen = display_surface
			self.clock = pygame.time.Clock()
			self.space = pymunk.Space()
			self.space.gravity = (0,500)
		def render(self):
			self.space.step(1/50)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
			self.screen.fill(self.bg_color)
			for objects in self.game_objects:
				objects.object_process()
				if objects.object_instance != "none":
					rotated_obj = pygame.transform.rotate(objects.object_instance, objects.transform.rotation)
					self.screen.blit(pygame.transform.scale(rotated_obj, (objects.transform.scale.x,objects.transform.scale.y)), objects.object_coord)
			pygame.display.update()
			self.clock.tick(self.frame_rate)

		class RigidBody:
			def __init__(self):
				pass






		class GameObject:
			def __init__(self, obj_name="default object", owntype="Sprite", static=False):
				self.name = obj_name
				self.type = owntype
				self.object_coord = [0,0]
				self.object_instance = "none"
				self.transform = self.Transform()
				self.attributes = self.Attributes()
				self.velocity_y = 0

			def object_process(self):
				
				self.object_coord[0] = self.transform.position.x
				self.object_coord[1] = self.transform.position.y

				

				


				currentindex = 0
				for proberty in self.attributes.attribute_names:
					if proberty == "Gravity":
						if self.attributes.attributes[currentindex].static == False:
							self.velocity_y += 0.5 * self.attributes.attributes[currentindex].mass
					if proberty == "PhysicsObject":
						self.transform.position.x = int(self.attributes.attributes[currentindex].body.position.x)
						self.transform.position.y = int(self.attributes.attributes[currentindex].body.position.y)
					
					currentindex += 1
				self.transform.position.y += self.velocity_y

				


			def add_property(self, argument="texture",path=""):
				if self.type == "Sprite":
					self.object_instance = pygame.image.load(path)
			class Transform:
				def __init__(self):
					scale_tuple = namedtuple("scale", ["x","y"])
					position_tuple = namedtuple("position", ["x","y"])
					self.scale = scale_tuple
					self.scale.x = 200
					self.scale.y = 200
					self.rotation = 0
					self.position = position_tuple
					self.position.x = 0
					self.position.y = 0
			def apply_force(self, force=()):
				currentindex = 0
				for each in self.attributes.attribute_names:
					if each == "PhysicsObject":
						print("tried")
						self.attributes.attributes[currentindex].body.apply_force_at_world_point((force[0]*1000,force[1]*1000), self.attributes.attributes[currentindex].body.position)
					currentindex += 1


			class Attributes:
				def __init__(self):
					self.attributes = []
					self.attribute_names = []
				class MovementController:
					def __init__(self,movement="plattformer", jumping=True, left_key=pygame.K_a, right_key=pygame.K_d, up_key=pygame.K_w, down_key=pygame.K_s, jump_key=pygame.K_SPACE):
						self.settings = {}
				class Gravity:
					def __init__(self,mass=1,static=False):
						self.static = static
						self.mass = mass
				class PhysicsObject:
					def __init__(self, position=(0, 0), static=False, mass=1, inertia=100, own_size=(100, 100), space_path=0):
					    
						# Calculate half the size for convenience
						half_width = float(own_size[0] / 2)
						half_height = float(own_size[1] / 2)

						# Define the vertices of the square
						vertices = [(-half_width, -half_height),
						(-half_width, half_height),
						(half_width, half_height),
						(half_width, -half_height)]

						if static == False:
							self.body = pymunk.Body(mass, inertia, body_type=pymunk.Body.DYNAMIC)
						else:
							self.body = pymunk.Body(mass, inertia, body_type=pymunk.Body.STATIC)
						self.body.position = position
						self.shape = pymunk.Poly(self.body, vertices)


						self.shape.friction = 0.5  

						# Add damping to the body
						self.body.angular_damping = 0.1  
						self.body.linear_damping = 0.2  

						space_path.add(self.body, self.shape)
 


		




#default setup

engine = Engine("new project")
engine.engine_config([1000,800],"new project",60)

new_scene = engine.Scene("new_scene", 60, engine.screen)

#its x*1,6 to get rid of disparancy

#creating the player
player = new_scene.GameObject("player", "Sprite",False)
player.add_property("texture", "src/icons/delete.png")
player.transform.scale.x = 200
player.transform.scale.y = 200
player.attributes.attributes.append(player.attributes.PhysicsObject(position=(50,0),static=False, own_size=(300,300), space_path=new_scene.space))
player.attributes.attribute_names.append("PhysicsObject")


#create the floor
floor = new_scene.GameObject("floor", "Sprite",True)
floor.transform.scale.x = 400
floor.transform.scale.y = 60
floor.add_property("texture", "ground.png")
floor.attributes.attributes.append(floor.attributes.PhysicsObject(position=(10,600), static=True, own_size=(640,100), space_path=new_scene.space))
floor.attributes.attribute_names.append("PhysicsObject")







#rendering

new_scene.game_objects.append(player)
new_scene.game_objects.append(floor)

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				player.apply_force((0,-20))
			if event.key == pygame.K_d:
				player.apply_force((5, 0))
			if event.key == pygame.K_a:
				player.apply_force((-5, 0))
		
	new_scene.render()


