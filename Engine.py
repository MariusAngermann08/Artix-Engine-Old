import pygame
import sys
from ArtixPhysicsEngine.Vector2D import *
from InputMap import input_map

class Engine:
	def __init__(self, title="DefaultProject", res=[800,600], fps=60):
		self.title = title
		self.res = (res[0],res[1])
		self.fps = fps
		self.setup()
		self.prepare_defaults()
	def setup(self):
		self.screen = pygame.display.set_mode(self.res)
		pygame.display.set_caption(self.title)
		self.clock = pygame.time.Clock()
		self.methods = []
		self.events = []
	def prepare_defaults(self):
		self.scenes = []
		self.scene_map = {}
		self.current_scene = "None"
		self.next_scene_index = 0
	def handle_events(self):
		self.events = pygame.event.get()
		for event in self.events:
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
	def key_pressed(self, key):
		for event in self.events:
			if event.type == pygame.KEYDOWN:
				if event.key == input_map[key]: return True
	def run(self):
		if self.current_scene != "None":
			while True:
				self.handle_events()
				for func in self.methods:
					func(self)
				self.scenes[self.scene_map[self.current_scene]].render()
				pygame.display.update()
				self.clock.tick(self.fps)
	def addScene(self, scene_object):
		scene_object.engine_reference = self
		self.scenes.append(scene_object)
		self.scene_map[scene_object.name] = self.next_scene_index
		self.next_scene_index += 1
	def loadScene(self, scene_name):
		self.current_scene = scene_name
	def addMethod(self, method):
		self.methods.append(method)
	def key_pressed(self, key):
		check = False
		for event in self.events:
			if event.type == pygame.KEYDOWN:
				if event.key == input_map[key]:
					check = True
		return check
	class Scene:
		def __init__(self, name, bgcolor=(255,255,255)):
			self.name = name
			self.bgcolor = bgcolor
			self.setup()
		def setup(self):
			self.game_objects = []
			self.objects_map = {}
			self.next_object_index = 0
			self.engine_reference = None
			self.camera_pos = (0,0)
		def render(self):
			self.engine_reference.screen.fill(self.bgcolor)
			for obj in self.game_objects:
				obj.run_methods()
				obj.draw(self.engine_reference.screen, self)
		def addObject(self, object_source):
			object_source.engine_reference = self.engine_reference
			self.game_objects.append(object_source)
			self.objects_map[object_source.name] = self.next_object_index
			self.next_object_index += 1
		def getObject(self, object_name):
			return self.game_objects[self.objects_map[object_name]]
	class GameObject:
		def __init__(self, name, textures=[]):
			self.setup()
			self.name = name
			self.image_textures = textures
			if len(self.image_textures) != 0: self.src = pygame.image.load(self.image_textures[0])
		def setup(self):
			self.engine_reference = None
			self.image_textures = []
			self.position = self.Position(0,0)
			self.rotation = self.Rotation(0)
			self.scale = self.Scale(100,100)
			self.methods = []
		def run_methods(self):
			for func in self.methods:
				func(self, self.engine_reference)
		def draw(self, display_surface, scene_reference):
			if len(self.image_textures) != 0:
				display_surface.blit(pygame.transform.scale(pygame.transform.rotate(self.src, self.rotation.angle), (self.scale.x,self.scale.y)), (self.position.x-scene_reference.camera_pos[0],self.position.y-scene_reference.camera_pos[1]))
		def move(self, vector=[0,0]):
			self.position.x += vector[0]
			self.position.y += vector[1]
		def addMethod(self, method):
			self.methods.append(method)
		class Position:
			def __init__(self,x,y):
				self.x = x
				self.y = y
			def get(self):
				return [self.x,self.y]
			def set(self, pos=[0,0]):
				self.x, self.y = pos[0],pos[1]
		class Rotation:
			def __init__(self, angle):
				self.angle = angle
			def get(self):
				return self.angle
			def set(self, angle):
				self.angle = angle
		class Scale:
			def __init__(self,x,y):
				self.x = x
				self.y = y
			def get(self):
				return [self.x,self.y]
			def set(self, scale):
				self.x, self.y = scale[0],scale[1]
	class Method:
		def __init__(self, funcs={}):
			self.on_start = funcs["on_start"]
			self.update = funcs["update"]
			self.main = funcs["main"]



if __name__ == "__main__":
	engine = Engine("Engine Beta Test", [1000,800], 60)

	Level01 = engine.Scene("Level01", (255,255,255))
	box = engine.GameObject("box", ["src/box.jpeg"])
	ball = engine.GameObject("ball", ["src/ball.png"])
	ball.position.x = 500
	Level01.addObject(box)
	Level01.addObject(ball)

	def boxComponent(self, engine):
		self.move([1,0])

	box.addMethod(boxComponent)

	engine.addScene(Level01)
	engine.loadScene("Level01")
	engine.run()