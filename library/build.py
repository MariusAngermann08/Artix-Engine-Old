import pygame
import pymunk
import sys
import math
from collections import namedtuple

from Engine import Engine

engine = Engine("NicksGame")
engine.engine_config([800,600],"NicksGame",60)

DefaultScene = engine.Scene("DefaultScene", 60, engine.screen)
Player = DefaultScene.GameObject("Player", "Sprite", False)
Player.add_property("texture", "src/player.png")
Player.transform.scale.x = 180
Player.transform.scale.y = 180
Player.transform.position.x = 217
Player.transform.position.y = 268
DefaultScene.game_objects.append(Player)

Plattform1 = DefaultScene.GameObject("Plattform1", "Sprite", False)
Plattform1.add_property("texture", "src/plattform.png")
Plattform1.transform.scale.x = 260
Plattform1.transform.scale.y = 180
Plattform1.transform.position.x = 228
Plattform1.transform.position.y = 372
DefaultScene.game_objects.append(Plattform1)

Plattform2 = DefaultScene.GameObject("Plattform2", "Sprite", False)
Plattform2.add_property("texture", "src/spikes_plattform.png")
Plattform2.transform.scale.x = 260
Plattform2.transform.scale.y = 230
Plattform2.transform.position.x = 415
Plattform2.transform.position.y = 311
DefaultScene.game_objects.append(Plattform2)

Plattform3 = DefaultScene.GameObject("Plattform3", "Sprite", False)
Plattform3.add_property("texture", "src/plattform.png")
Plattform3.transform.scale.x = 260
Plattform3.transform.scale.y = 180
Plattform3.transform.position.x = 615
Plattform3.transform.position.y = 362
DefaultScene.game_objects.append(Plattform3)

while True:
	events = []
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			events.append(event)
	DefaultScene.render(events)
