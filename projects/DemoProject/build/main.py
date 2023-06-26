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
Player.transform.position.x = 395.6363636363636
Player.transform.position.y = 68.57142857142857
DefaultScene.game_objects.append(Player)
Player.attributes.attributes.append(Player.attributes.PhysicsObject(Player,position=(395.6363636363636,68.57142857142857),static=False,own_size=(109.0909090909091,123.8095238095238), space_path=DefaultScene.space, mass=1,inertia=100))
Player.attributes.attribute_names.append("PhysicsObject")
Player.eventsystem.root_node.append(Player.eventsystem.Event(Player,DefaultScene,"keypress","Space"))
Player.eventsystem.root_node[0].actions.append(Player.eventsystem.Action(Player,DefaultScene,engine,"applyforce","0", "-20"))
Player.eventsystem.root_node.append(Player.eventsystem.Event(Player,DefaultScene,"keyhold","a"))
Player.eventsystem.root_node[1].actions.append(Player.eventsystem.Action(Player,DefaultScene,engine,"applyforce","-1", "0"))
Player.eventsystem.root_node.append(Player.eventsystem.Event(Player,DefaultScene,"keyhold","d"))
Player.eventsystem.root_node[2].actions.append(Player.eventsystem.Action(Player,DefaultScene,engine,"applyforce","1", "0"))

floor = DefaultScene.GameObject("floor", "Sprite", False)
floor.add_property("texture", "src/ground.png")
floor.transform.scale.x = 290.90909090909093
floor.transform.scale.y = 123.8095238095238
floor.transform.position.x = 16.72727272727272
floor.transform.position.y = 454.2857142857143
DefaultScene.game_objects.append(floor)
floor.attributes.attributes.append(floor.attributes.PhysicsObject(floor,position=(16.72727272727272,454.2857142857143),static=True,own_size=(290.90909090909093,123.8095238095238), space_path=DefaultScene.space, mass=1,inertia=100))
floor.attributes.attribute_names.append("PhysicsObject")

fllor2 = DefaultScene.GameObject("fllor2", "Sprite", False)
fllor2.add_property("texture", "src/ground.png")
fllor2.transform.scale.x = 181.8181818181818
fllor2.transform.scale.y = 123.8095238095238
fllor2.transform.position.x = 390.5454545454546
fllor2.transform.position.y = 286.66666666666663
DefaultScene.game_objects.append(fllor2)
fllor2.attributes.attributes.append(fllor2.attributes.PhysicsObject(fllor2,position=(390.5454545454546,286.66666666666663),static=True,own_size=(181.8181818181818,123.8095238095238), space_path=DefaultScene.space, mass=1,inertia=100))
fllor2.attributes.attribute_names.append("PhysicsObject")

Goal = DefaultScene.GameObject("Goal", "Sprite", False)
Goal.add_property("texture", "src/blue.png")
Goal.transform.scale.x = 72.72727272727273
Goal.transform.scale.y = 95.23809523809523
Goal.transform.position.x = 734.5454545454545
Goal.transform.position.y = 153.33333333333331
DefaultScene.game_objects.append(Goal)
Goal.eventsystem.root_node.append(Goal.eventsystem.Event(Goal,DefaultScene,"colwith","Player"))
Goal.eventsystem.root_node[0].actions.append(Goal.eventsystem.Action(Goal,DefaultScene,engine,"loadscene","Level2"))

Level2 = engine.Scene("Level2", 60, engine.screen)
engine.scenes.append(Level2)
Player2 = Level2.GameObject("Player2", "Sprite", False)
Player2.add_property("texture", "src/blue.png")
Player2.transform.scale.x = 101.81818181818183
Player2.transform.scale.y = 133.33333333333331
Player2.transform.position.x = 109.81818181818181
Player2.transform.position.y = 234.28571428571428
Level2.game_objects.append(Player2)
Player2.eventsystem.root_node.append(Player2.eventsystem.Event(Player2,Level2,"keyhold","a"))
Player2.eventsystem.root_node[0].actions.append(Player2.eventsystem.Action(Player2,Level2,engine,"move","-5", "0"))
Player2.eventsystem.root_node.append(Player2.eventsystem.Event(Player2,Level2,"keyhold","d"))
Player2.eventsystem.root_node[1].actions.append(Player2.eventsystem.Action(Player2,Level2,engine,"move","5", "0"))
Player2.eventsystem.root_node.append(Player2.eventsystem.Event(Player2,Level2,"keyhold","w"))
Player2.eventsystem.root_node[2].actions.append(Player2.eventsystem.Action(Player2,Level2,engine,"move","0", "-5"))
Player2.eventsystem.root_node.append(Player2.eventsystem.Event(Player2,Level2,"keyhold","s"))
Player2.eventsystem.root_node[3].actions.append(Player2.eventsystem.Action(Player2,Level2,engine,"move","0", "5"))

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
