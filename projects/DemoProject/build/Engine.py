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
			self.scenes = []
			self.currentscene = 0
		except:
			print("Engine initialization failed")
	def engine_controller(self):
		pass
	def engine_config(self,window_size=[600,300],window_caption="default caption",new_frame_rate=60):
		self.render_size = (window_size[0],window_size[1])
		self.render_caption = window_caption
		self.frame_rate = new_frame_rate
		self.screen = pygame.display.set_mode(self.render_size)
		pygame.display.set_caption(self.render_caption)
	def run(self, ev1=None):
		self.scenes[self.currentscene].render(ev1)

	class Scene:
		game_objects = []
		rigid_bodies = []
		def __init__(self, scene_name="default scene", engine_frame_rate=60, display_surface=0, global_gravity=(0,500), bgcolor=(255,255,255)):
			self.name = scene_name
			self.frame_rate = engine_frame_rate
			self.bg_color = bgcolor
			self.screen = display_surface
			self.clock = pygame.time.Clock()
			self.space = pymunk.Space()
			self.space.gravity = (0,500)
			self.game_objects = []
		def render(self,ev=None):
			self.space.step(1/50)
			self.screen.fill(self.bg_color)

			for objects in self.game_objects:
				objects.object_process(ev)
				if objects.object_instance != "none":
					rotated_obj = pygame.transform.rotate(objects.object_instance, objects.transform.rotation)
					self.screen.blit(pygame.transform.scale(rotated_obj, (objects.transform.scale.x,objects.transform.scale.y)), [objects.object_coord[0],objects.object_coord[1]])
					#-(objects.transform.scale.x/2.083)
				
			pygame.display.update()
			self.clock.tick(self.frame_rate)

		class GameObject:
			def __init__(self, obj_name="default object", owntype="Sprite", static=False):
				self.name = obj_name
				self.type = owntype
				self.object_coord = [0,0]
				self.object_instance = "none"
				self.transform = self.Transform()
				self.attributes = self.Attributes(self)
				self.velocity_y = 0
				self.eventsystem = self.EventSystem(self)


			class EventSystem:
				def __init__(self, rootlink=None):
					self.root_node = []
					self.root = rootlink
				def process(self, pro=None):
					for events in self.root_node:
						events.check(pro)
				class Event:
					def __init__(self,obj_link=None,scenelink=None,own_type="",argument1="",argument2=""):
						self.actions = []
						self.events = []
						self.type = own_type
						self.argument1 = argument1
						self.argument2 = argument2
						self.object = obj_link
						self.scene = scenelink
						self.hold = False
					def check(self, k=None):
						if self.type == "keypress":
							keymap = {
								"UP": pygame.K_UP,
								"DOWN": pygame.K_DOWN,
								"RIGHT": pygame.K_RIGHT,
								"LEFT": pygame.K_LEFT,
								"a": pygame.K_a,
								"b": pygame.K_b,
								"c": pygame.K_c,
								"d": pygame.K_d,
								"e": pygame.K_e,
								"f": pygame.K_f,
								"g": pygame.K_g,
								"h": pygame.K_h,
								"i": pygame.K_i,
								"j": pygame.K_j,
								"k": pygame.K_k,
								"l": pygame.K_l,
								"m": pygame.K_m,
								"n": pygame.K_n,
								"o": pygame.K_o,
								"p": pygame.K_p,
								"q": pygame.K_q,
								"r": pygame.K_r,
								"s": pygame.K_s,
								"t": pygame.K_t,
								"u": pygame.K_u,
								"v": pygame.K_v,
								"w": pygame.K_w,
								"x": pygame.K_x,
								"y": pygame.K_y,
								"z": pygame.K_z,
								"Space": pygame.K_SPACE
							}
							for i in k:
								if i.type == pygame.KEYDOWN:
									if i.key == keymap[self.argument1]:
										print("ran")
										for a in self.actions:
											a.run()
										for a in self.events:
											a.check()
						elif self.type == "keyhold":
							keymap = {
								"UP": pygame.K_UP,
								"DOWN": pygame.K_DOWN,
								"RIGHT": pygame.K_RIGHT,
								"LEFT": pygame.K_LEFT,
								"a": pygame.K_a,
								"b": pygame.K_b,
								"c": pygame.K_c,
								"d": pygame.K_d,
								"e": pygame.K_e,
								"f": pygame.K_f,
								"g": pygame.K_g,
								"h": pygame.K_h,
								"i": pygame.K_i,
								"j": pygame.K_j,
								"k": pygame.K_k,
								"l": pygame.K_l,
								"m": pygame.K_m,
								"n": pygame.K_n,
								"o": pygame.K_o,
								"p": pygame.K_p,
								"q": pygame.K_q,
								"r": pygame.K_r,
								"s": pygame.K_s,
								"t": pygame.K_t,
								"u": pygame.K_u,
								"v": pygame.K_v,
								"w": pygame.K_w,
								"x": pygame.K_x,
								"y": pygame.K_y,
								"z": pygame.K_z,
								"Space": pygame.K_SPACE
							}

							if self.hold == True:
								for a in self.actions:
									a.run()
								for a in self.events:
									a.check()
								

							for i in k:
								if i.type == pygame.KEYDOWN:
									if i.key == keymap[self.argument1]:
										self.hold = True
								if i.type == pygame.KEYUP:
									if i.key == keymap[self.argument1]:
										self.hold = False
										

							



						if self.type == "colwith":
							search = 0
							currentindex = 0
							for objs in self.scene.game_objects:
								if objs.name == self.argument1:
									search = currentindex
									break
								currentindex += 1

							objectx = self.object.object_coord[0]
							objecty = self.object.object_coord[1]
							objectwidth = self.object.transform.scale.x
							objectheight = self.object.transform.scale.y

							otherx = self.scene.game_objects[search].object_coord[0]
							othery = self.scene.game_objects[search].object_coord[1]
							otherwidth = self.scene.game_objects[search].transform.scale.x
							otherheight = self.scene.game_objects[search].transform.scale.y

							obj1_top_left = [objectx,objecty]
							obj1_bottom_right = [objectx + objectwidth, objecty + objectheight]

							obj2_top_left = [otherx,othery]
							obj2_bottom_right = [otherx + otherwidth, othery + otherheight]

							if obj1_bottom_right[0] >= obj2_top_left[0] and obj2_bottom_right[0] >= obj1_top_left[0]:
								if obj1_bottom_right[1] >= obj2_top_left[1] and obj2_bottom_right[1] >= obj1_top_left[1]:
									for a in self.actions:
										a.run()
									for a in self.events:
										a.check()

						if self.type == "colbtw":

							search1 = 0
							currentindex = 0
							for objs in self.scene.game_objects:
								if objs.name == self.argument1:
									search1 = currentindex
									break
								currentindex += 1

							search2 = 0
							currentindex = 0
							for objs in self.scene.game_objects:
								if objs.name == self.argument2:
									search2 = currentindex
									break
								currentindex += 1



							objectx = self.scene.game_objects[search1].object_coord[0]
							objecty = self.scene.game_objects[search1].object_coord[1]
							objectwidth = self.scene.game_objects[search1].transform.scale.x
							objectheight = self.scene.game_objects[search1].transform.scale.y

							otherx = self.scene.game_objects[search2].object_coord[0]
							othery = self.scene.game_objects[search2].object_coord[1]
							otherwidth = self.scene.game_objects[search2].transform.scale.x
							otherheight = self.scene.game_objects[search2].transform.scale.y

							obj1_top_left = [objectx,objecty]
							obj1_bottom_right = [objectx + objectwidth, objecty + objectheight]

							obj2_top_left = [otherx,othery]
							obj2_bottom_right = [otherx + otherwidth, othery + otherheight]

							if obj1_bottom_right[0] >= obj2_top_left[0] and obj2_bottom_right[0] >= obj1_top_left[0]:
								if obj1_bottom_right[1] >= obj2_top_left[1] and obj2_bottom_right[1] >= obj1_top_left[1]:
									for a in self.actions:
										a.run()
									for a in self.events:
										a.check()



				class Action:
					def __init__(self,rootlink=None,scenelink=None,enginelink=None, owntype="", argument1="", argument2="", argument3=""):
						self.type = owntype
						self.argument1 = argument1
						self.argument2 = argument2
						self.argument3 = argument3
						self.root = rootlink
						self.scene = scenelink
						self.engine = enginelink
					def run(self):
						if self.type == "print":
							print(self.argument1)
						elif self.type == "applyforce":
							self.root.apply_force((int(self.argument1),int(self.argument2)))
						elif self.type == "setpos":
							if "PhysicsObject" in self.root.attributes.attribute_names:
								self.root.body.position = (int(self.argument1),int(self.argument2))
							else:
								self.root.transform.position.x = int(self.argument1)
								self.root.transform.position.y = int(self.argument2)
						elif self.type == "move":
							if "PhysicsObject" in self.root.attributes.attribute_names:
								self.root.body.position = (self.root.body.position[0]+int(self.argument1),self.root.body.position[1]+int(self.argument2))
							else:
								self.root.transform.position.x = self.root.transform.position.x+int(self.argument1)
								self.root.transform.position.y = self.root.transform.position.y+int(self.argument2)
						elif self.type == "setobjpos":
							currentindex = 0
							search = 0
							for objs in self.scene.game_objects:
								if objs.name == self.argument1:
									search = currentindex
									break
								currentindex += 1

							if "PhysicsObject" in self.scene.game_objects[search].attributes.attribute_names:
								self.scene.game_objects[search].body.position = (int(self.argument2),int(self.argument3))
							else:
								self.scene.game_objects[search].transform.position.x = int(self.argument2)
								self.scene.game_objects[search].transform.position.y = int(self.argument3)
						elif self.type == "moveobj":
							currentindex = 0
							search = 0
							for objs in self.scene.game_objects:
								if objs.name == self.argument1:
									search = currentindex
									break
								currentindex += 1

							if "PhysicsObject" in self.scene.game_objects[search].attributes.attribute_names:
								self.scene.game_objects[search].body.position = (self.scene.game_objects[search].body.position[0]+int(self.argument2),self.scenes.game_objects[search].body.position[1]+int(self.argument3))
							else:
								self.scene.game_objects[search].object_coord[0] = self.scene.game_objects[search].object_coord[0]+int(self.argument2)
								self.scene.game_objects[search].object_coord[1] = self.scene.game_objects[search].object_coord[1]+int(self.argument3)

						elif self.type == "loadscene":
							search = 0
							currentindex = 0
							for scene in self.engine.scenes:
								if scene.name == self.argument1:
									search = currentindex
									break
								currentindex += 1
							self.engine.currentscene = search


			def object_process(self, event1=None):

				self.eventsystem.process(event1)


				self.object_coord[0] = self.transform.position.x
				self.object_coord[1] = self.transform.position.y

				

				


				currentindex = 0
				for proberty in self.attributes.attribute_names:
					if proberty == "Gravity":
						if self.attributes.attributes[currentindex].static == False:
							self.velocity_y += 0.5 * self.attributes.attributes[currentindex].mass
					if proberty == "PhysicsObject":
						self.transform.position.x = self.attributes.attributes[currentindex].body.position.x
						self.transform.position.y = self.attributes.attributes[currentindex].body.position.y
					
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
				def __init__(self, root=None):
					self.attributes = []
					self.root = root
					self.attribute_names = []
				class MovementController:
					def __init__(self,movement="plattformer", jumping=True, left_key=pygame.K_a, right_key=pygame.K_d, up_key=pygame.K_w, down_key=pygame.K_s, jump_key=pygame.K_SPACE):
						self.settings = {}
				class Gravity:
					def __init__(self,mass=1,static=False):
						self.static = static
						self.mass = mass
				class PhysicsObject:
					def __init__(self, rootnode=None, position=(0, 0), static=False, mass=1, inertia=100, own_size=(100, 100), space_path=0):
						self.root = rootnode

						

						if not static:
							self.body = pymunk.Body(mass, inertia, body_type=pymunk.Body.DYNAMIC)
						else:
							self.body = pymunk.Body(mass, inertia, body_type=pymunk.Body.STATIC)

						# Set the position of the body directly
						self.body.position = (position[0]+(own_size[0]/2),position[1]+(own_size[1]/2))

						self.shape = pymunk.Poly.create_box(self.body, size=(own_size[0]+(own_size[0]/6), own_size[1]))



						self.shape.friction = 0.5

						# Add damping to the body
						self.body.angular_damping = 0.1
						self.body.linear_damping = 0.2

						self.root.body = self.body
						self.root.shape = self.shape

						space_path.add(self.body, self.shape)
