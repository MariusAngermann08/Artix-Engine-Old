import pygame
import pymunk
import sys
import math
from collections import namedtuple

from Engine import Engine

engine = Engine("blank")
engine.engine_config([800,600],"blank",60)

DefaultScene = engine.Scene("DefaultScene", 60, engine.screen)
engine.scenes.append(DefaultScene)
Player = DefaultScene.GameObject("Player", "Sprite", False)
Player.add_property("texture", "src/blue.png")
Player.transform.scale.x = 145.45454545454547
Player.transform.scale.y = 142.85714285714286
Player.transform.position.x = 53.81818181818181
Player.transform.position.y = 181.9047619047619
DefaultScene.game_objects.append(Player)
Player.attributes.attributes.append(Player.attributes.PhysicsObject(Player,position=(53.81818181818181,181.9047619047619),static=False,own_size=(145.45454545454547,142.85714285714286), space_path=DefaultScene.space, mass=1,inertia=100))
Player.attributes.attribute_names.append("PhysicsObject")
Player.eventsystem.root_node.append(Player.eventsystem.Event(Player,DefaultScene,"keypress","Space"))
Player.eventsystem.root_node[0].actions.append(Player.eventsystem.Action(Player,DefaultScene,engine,"applyforce","0", "-15"))
Player.eventsystem.root_node.append(Player.eventsystem.Event(Player,DefaultScene,"keyhold","a"))
Player.eventsystem.root_node[1].actions.append(Player.eventsystem.Action(Player,DefaultScene,engine,"applyforce","-1", "0"))
Player.eventsystem.root_node.append(Player.eventsystem.Event(Player,DefaultScene,"keyhold","d"))
Player.eventsystem.root_node[2].actions.append(Player.eventsystem.Action(Player,DefaultScene,engine,"applyforce","1", "0"))

Floor = DefaultScene.GameObject("Floor", "Sprite", False)
Floor.add_property("texture", "src/blue.png")
Floor.transform.scale.x = 400.0
Floor.transform.scale.y = 104.76190476190476
Floor.transform.position.x = 15.27272727272728
Floor.transform.position.y = 432.38095238095235
DefaultScene.game_objects.append(Floor)
Floor.attributes.attributes.append(Floor.attributes.PhysicsObject(Floor,position=(15.27272727272728,432.38095238095235),static=True,own_size=(400.0,104.76190476190476), space_path=DefaultScene.space, mass=1,inertia=100))
Floor.attributes.attribute_names.append("PhysicsObject")

End = DefaultScene.GameObject("End", "Sprite", False)
End.add_property("texture", "src/ground.png")
End.transform.scale.x = 50.909090909090914
End.transform.scale.y = 66.66666666666666
End.transform.position.x = 754.1818181818181
End.transform.position.y = 259.04761904761904
DefaultScene.game_objects.append(End)

cube = DefaultScene.GameObject("cube", "Sprite", False)
cube.add_property("texture", "src/ground.png")
cube.transform.scale.x = 130.9090909090909
cube.transform.scale.y = 171.42857142857142
cube.transform.position.x = 548.3636363636364
cube.transform.position.y = 316.19047619047615
DefaultScene.game_objects.append(cube)
cube.attributes.attributes.append(cube.attributes.PhysicsObject(cube,position=(548.3636363636364,316.19047619047615),static=True,own_size=(130.9090909090909,171.42857142857142), space_path=DefaultScene.space, mass=1,inertia=100))
cube.attributes.attribute_names.append("PhysicsObject")

Level2 = engine.Scene("Level2", 60, engine.screen)
engine.scenes.append(Level2)
while True:
	events = []
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			events.append(event)
		if event.type == pygame.KEYUP:
			events.append(event)
	engine.run(events)
