


		




#default setup

engine = Engine("new project")
engine.engine_config([1000,800],"new project",60)

new_scene = engine.Scene("new_scene", 60, engine.screen)
engine.scenes.append(new_scene)

#its x*1,6 to get rid of disparancy

#creating the player
player = new_scene.GameObject("player", "Sprite",False)
player.add_property("texture", "src/icons/delete.png")
player.transform.scale.x = 200
player.transform.scale.y = 200
player.transform.position.x = 50
player.transform.position.y = 50
player.attributes.attributes.append(player.attributes.PhysicsObject(player,position=(50,0),static=False, own_size=(200,200), space_path=new_scene.space))
player.attributes.attribute_names.append("PhysicsObject")


#create the floor
floor = new_scene.GameObject("floor", "Sprite",True)
floor.transform.scale.x = 400
floor.transform.scale.y = 60
player.transform.position.x = 10
player.transform.position.y = 600
floor.add_property("texture", "ground.png")
floor.attributes.attributes.append(floor.attributes.PhysicsObject(floor,position=(10,600), static=True, own_size=(400,60), space_path=new_scene.space))
floor.attributes.attribute_names.append("PhysicsObject")



#events
player.eventsystem.root_node.append(player.eventsystem.Event(player, new_scene, "keyhold","l"))
player.eventsystem.root_node[0].actions.append(player.eventsystem.Action(player,new_scene,engine, "setobjpos", "floor", "10", "10"))




#rendering

new_scene.game_objects.append(player)
new_scene.game_objects.append(floor)

new = engine.Scene("new", 60, engine.screen)
engine.scenes.append(new)


running = True
while running:
	events = []
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
			events.append(event)
		if event.type == pygame.KEYUP:
			events.append(event)

	print(engine.currentscene)
	engine.run(events)
		
	



