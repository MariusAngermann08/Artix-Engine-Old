import pygame
import pymunk
import sys
import math
from collections import namedtuple

from Engine import Engine

engine = Engine("DemoProject")
engine.engine_config([800,600],"DemoProject",60)

DefaultScene = engine.Scene("DefaultScene", 60, engine.screen, bgcolor=(108,184,213))
engine.scenes.append(DefaultScene)
House = DefaultScene.GameObject("House", "Sprite", False)
House.add_property("texture", "src/base.png")
House.transform.scale.x = 181.8181818181818
House.transform.scale.y = 238.09523809523807
House.transform.position.x = 613.8181818181819
House.transform.position.y = 341.90476190476187
DefaultScene.game_objects.append(House)

Player = DefaultScene.GameObject("Player", "Sprite", False)
Player.add_property("texture", "src/Idle (1).png")
Player.transform.scale.x = 130.9090909090909
Player.transform.scale.y = 171.42857142857142
Player.transform.position.x = 48.0
Player.transform.position.y = 388.57142857142856
DefaultScene.game_objects.append(Player)
Player.eventsystem.root_node.append(Player.eventsystem.Event(Player,DefaultScene,"keyhold","a"))
Player.eventsystem.root_node[0].actions.append(Player.eventsystem.Action(Player,DefaultScene,engine,"move","-3", "0"))
Player.eventsystem.root_node.append(Player.eventsystem.Event(Player,DefaultScene,"keyhold","d"))
Player.eventsystem.root_node[1].actions.append(Player.eventsystem.Action(Player,DefaultScene,engine,"move","3", "0"))
Player.eventsystem.root_node.append(Player.eventsystem.Event(Player,DefaultScene,"colwith","House"))
Player.eventsystem.root_node[2].actions.append(Player.eventsystem.Action(Player,DefaultScene,engine,"loadscene","PhysicsDemo"))

Title = DefaultScene.GameObject("Title", "Sprite", False)
Title.add_property("texture", "src/title.png")
Title.transform.scale.x = 727.2727272727273
Title.transform.scale.y = 95.23809523809523
Title.transform.position.x = 30.54545454545456
Title.transform.position.y = 67.61904761904762
DefaultScene.game_objects.append(Title)

PhysicsDemo = engine.Scene("PhysicsDemo", 60, engine.screen, bgcolor=(133,194,126))
engine.scenes.append(PhysicsDemo)
Floor1 = PhysicsDemo.GameObject("Floor1", "Sprite", False)
Floor1.add_property("texture", "src/ground.png")
Floor1.transform.scale.x = 363.6363636363636
Floor1.transform.scale.y = 171.42857142857142
Floor1.transform.position.x = -138.9090909090909
Floor1.transform.position.y = 429.5238095238095
PhysicsDemo.game_objects.append(Floor1)
Floor1.attributes.attributes.append(Floor1.attributes.PhysicsObject(Floor1,position=(-138.9090909090909,429.5238095238095),static=True,own_size=(363.6363636363636,171.42857142857142), space_path=PhysicsDemo.space, mass=1,inertia=100))
Floor1.attributes.attribute_names.append("PhysicsObject")

Player = PhysicsDemo.GameObject("Player", "Sprite", False)
Player.add_property("texture", "src/Idle (1).png")
Player.transform.scale.x = 130.9090909090909
Player.transform.scale.y = 171.42857142857142
Player.transform.position.x = -31.272727272727273
Player.transform.position.y = 147.61904761904762
PhysicsDemo.game_objects.append(Player)
Player.attributes.attributes.append(Player.attributes.PhysicsObject(Player,position=(-31.272727272727273,147.61904761904762),static=False,own_size=(130.9090909090909,171.42857142857142), space_path=PhysicsDemo.space, mass=1,inertia=100))
Player.attributes.attribute_names.append("PhysicsObject")
Player.eventsystem.root_node.append(Player.eventsystem.Event(Player,PhysicsDemo,"keypress","Space"))
Player.eventsystem.root_node[0].actions.append(Player.eventsystem.Action(Player,PhysicsDemo,engine,"applyforce","0", "-20"))
Player.eventsystem.root_node.append(Player.eventsystem.Event(Player,PhysicsDemo,"keyhold","a"))
Player.eventsystem.root_node[1].actions.append(Player.eventsystem.Action(Player,PhysicsDemo,engine,"move","-5", "0"))
Player.eventsystem.root_node.append(Player.eventsystem.Event(Player,PhysicsDemo,"keyhold","d"))
Player.eventsystem.root_node[2].actions.append(Player.eventsystem.Action(Player,PhysicsDemo,engine,"move","5", "0"))

Floor2 = PhysicsDemo.GameObject("Floor2", "Sprite", False)
Floor2.add_property("texture", "src/ground.png")
Floor2.transform.scale.x = 363.6363636363636
Floor2.transform.scale.y = 171.42857142857142
Floor2.transform.position.x = 237.09090909090912
Floor2.transform.position.y = 490.4761904761904
PhysicsDemo.game_objects.append(Floor2)
Floor2.attributes.attributes.append(Floor2.attributes.PhysicsObject(Floor2,position=(237.09090909090912,490.4761904761904),static=True,own_size=(363.6363636363636,171.42857142857142), space_path=PhysicsDemo.space, mass=1,inertia=100))
Floor2.attributes.attribute_names.append("PhysicsObject")

End = engine.Scene("End", 60, engine.screen, bgcolor=(255,255,255))
engine.scenes.append(End)
BIG = End.GameObject("BIG", "Sprite", False)
BIG.add_property("texture", "src/star.png")
BIG.transform.scale.x = 218.1818181818182
BIG.transform.scale.y = 285.7142857142857
BIG.transform.position.x = 268.3636363636364
BIG.transform.position.y = 277.1428571428571
End.game_objects.append(BIG)

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
