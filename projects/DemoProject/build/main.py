import pygame
import pymunk
import sys
import math
from collections import namedtuple

from Engine import Engine

engine = Engine("DemoProject")
engine.engine_config([800,600],"DemoProject",60)

DefaultScene = engine.Scene("DefaultScene", 60, engine.screen)
engine.scenes.append(DefaultScene)
Player = DefaultScene.GameObject("Player", "Sprite", False)
Player.add_property("texture", "src/blue.png")
Player.transform.scale.x = 109.0909090909091
Player.transform.scale.y = 123.8095238095238
Player.transform.position.x = 96.72727272727273
Player.transform.position.y = 69.52380952380952
DefaultScene.game_objects.append(Player)
Player.attributes.attributes.append(Player.attributes.PhysicsObject(Player,position=(96.72727272727273,69.52380952380952),static=False,own_size=(174.54545454545456,123.8095238095238), space_path=DefaultScene.space, mass=1,inertia=100))
Player.attributes.attribute_names.append("PhysicsObject")

floor = DefaultScene.GameObject("floor", "Sprite", False)
floor.add_property("texture", "src/ground.png")
floor.transform.scale.x = 363.6363636363636
floor.transform.scale.y = 123.8095238095238
floor.transform.position.x = 42.90909090909091
floor.transform.position.y = 486.66666666666663
DefaultScene.game_objects.append(floor)
floor.attributes.attributes.append(floor.attributes.PhysicsObject(floor,position=(42.90909090909091,486.66666666666663),static=True,own_size=(581.8181818181819,123.8095238095238), space_path=DefaultScene.space, mass=1,inertia=100))
floor.attributes.attribute_names.append("PhysicsObject")

secondfloor = DefaultScene.GameObject("secondfloor", "Sprite", False)
secondfloor.add_property("texture", "src/ground.png")
secondfloor.transform.scale.x = 181.8181818181818
secondfloor.transform.scale.y = 123.8095238095238
secondfloor.transform.position.x = 518.5454545454546
secondfloor.transform.position.y = 396.19047619047615
DefaultScene.game_objects.append(secondfloor)
secondfloor.attributes.attributes.append(secondfloor.attributes.PhysicsObject(secondfloor,position=(518.5454545454546,396.19047619047615),static=True,own_size=(290.90909090909093,123.8095238095238), space_path=DefaultScene.space, mass=1,inertia=100))
secondfloor.attributes.attribute_names.append("PhysicsObject")

while True:
	events = []
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			events.append(event)
	engine.run(events)
