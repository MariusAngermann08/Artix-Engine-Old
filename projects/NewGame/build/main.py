import pygame
import pymunk
import sys
import math
from collections import namedtuple

from Engine import Engine

engine = Engine("NewGame")
engine.engine_config([800,600],"NewGame",60)

DefaultScene = engine.Scene("DefaultScene", 60, engine.screen)
Player = DefaultScene.GameObject("Player", "Sprite", False)
Player.add_property("texture", "src/player.png")
Player.transform.scale.x = 180
Player.transform.scale.y = 180
Player.transform.position.x = 212
Player.transform.position.y = 288
DefaultScene.game_objects.append(Player)

Plattform1 = DefaultScene.GameObject("Plattform1", "Sprite", False)
Plattform1.add_property("texture", "src/plattform.png")
Plattform1.transform.scale.x = 260
Plattform1.transform.scale.y = 180
Plattform1.transform.position.x = 212
Plattform1.transform.position.y = 386
DefaultScene.game_objects.append(Plattform1)

Plattform2 = DefaultScene.GameObject("Plattform2", "Sprite", False)
Plattform2.add_property("texture", "src/spikes_plattform.png")
Plattform2.transform.scale.x = 260
Plattform2.transform.scale.y = 220
Plattform2.transform.position.x = 546
Plattform2.transform.position.y = 320
DefaultScene.game_objects.append(Plattform2)

while True:
	events = []
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			events.append(event)
	DefaultScene.render(events)
