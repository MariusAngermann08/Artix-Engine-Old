import pygame
import pymunk
import sys
import math
from collections import namedtuple

from Engine import Engine

engine = Engine("JumpAndRun")
engine.engine_config([800,600],"JumpAndRun",60)

DefaultScene = engine.Scene("DefaultScene", 60, engine.screen)
Player = DefaultScene.GameObject("Player", "Sprite", False)
Player.add_property("texture", "src/player.png")
Player.transform.scale.x = 160.0
Player.transform.scale.y = 171.42857142857142
Player.transform.position.x = 296.0
Player.transform.position.y = 232.38095238095238
DefaultScene.game_objects.append(Player)
Player.attributes.attributes.append(Player.attributes.PhysicsObject(position=(296.0,232.38095238095238),static=False,own_size=(256.0,171.42857142857142), space_path=DefaultScene.space, mass=1,inertia=100))
Player.attributes.attribute_names.append("PhysicsObject")

Plattform1 = DefaultScene.GameObject("Plattform1", "Sprite", False)
Plattform1.add_property("texture", "src/blue.png")
Plattform1.transform.scale.x = 218.1818181818182
Plattform1.transform.scale.y = 200.0
Plattform1.transform.position.x = 68.36363636363637
Plattform1.transform.position.y = 436.19047619047615
DefaultScene.game_objects.append(Plattform1)
Plattform1.attributes.attributes.append(Plattform1.attributes.PhysicsObject(position=(68.36363636363637,436.19047619047615),static=True,own_size=(349.0909090909091,200.0), space_path=DefaultScene.space, mass=1,inertia=100))
Plattform1.attributes.attribute_names.append("PhysicsObject")

while True:
	events = []
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			events.append(event)
	DefaultScene.render(events)
