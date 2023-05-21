# This is the main file the engine should be started with. It starts the project manager after a splash screen.
# Copyright (C) 2023 Marius Angermann
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.


import sys
import pygame
import subprocess
import os

pygame.init()

flag = pygame.NOFRAME

screen = pygame.display.set_mode((750,400), flag)

clock = pygame.time.Clock()

image = pygame.image.load("src/boot_up_logo.png")
image_render = pygame.transform.scale(image, (750,400))


textfont = pygame.font.SysFont("Aharoni",25)

loadingstring = "test load complete"

loading_states = [
	"preparing to start ",
	"preparing to start . ",
	"preparing to start .. ",
	"preparing to start ... "
]

currentstateindex = 0

script_dir = os.path.dirname(os.path.realpath(__file__))



frame_counter = 0
sec_gone = 0
while True:
	if sec_gone == 15:
		subprocess.Popen('cmd /c cd /d "{}" &'.format(script_dir), shell=True)
		subprocess.Popen('python project_manager.py', shell=True)
		pygame.quit()
		sys.exit()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	if frame_counter == 60 * 0.7:
		sec_gone += 1
		frame_counter = 0
		if currentstateindex == 3:
			currentstateindex = 0
		else:
			currentstateindex += 1

	loadinglabel = textfont.render(loading_states[currentstateindex],1,(255,255,255))

	screen.fill((0,0,0))
	screen.blit(image_render, (0,0))
	screen.blit(loadinglabel, (580,380))

	frame_counter += 1

	pygame.display.update()
	clock.tick(60)