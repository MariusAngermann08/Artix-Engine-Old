 


		




#default setup

engine = Engine("new project")
engine.engine_config([1000,800],"new project",60)

new_scene = engine.Scene("new_scene", 60, engine.screen)

#its x*1,6 to get rid of disparancy

#creating the player
player = new_scene.GameObject("player", "Sprite",False)
player.add_property("texture", "src/icons/delete.png")
player.transform.scale.x = 200
player.transform.scale.y = 200
player.attributes.attributes.append(player.attributes.PhysicsObject(position=(50,0),static=False, own_size=(300,300), space_path=new_scene.space))
player.attributes.attribute_names.append("PhysicsObject")


#create the floor
floor = new_scene.GameObject("floor", "Sprite",True)
floor.transform.scale.x = 400
floor.transform.scale.y = 60
floor.add_property("texture", "ground.png")
floor.attributes.attributes.append(floor.attributes.PhysicsObject(position=(10,600), static=True, own_size=(640,100), space_path=new_scene.space))
floor.attributes.attribute_names.append("PhysicsObject")



#events
player.eventsystem.root_node.append(player.eventsystem.Event("keypress","k"))
player.eventsystem.root_node[0].actions.append(player.eventsystem.Action(player.eventsystem.root,"apply_force", "0", "-20"))




#rendering

new_scene.game_objects.append(player)
new_scene.game_objects.append(floor)

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

	new_scene.render(events)
		
	


