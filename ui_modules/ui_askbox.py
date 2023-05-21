# This is the ui_askbox module it is made for the gui of the project manager
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



import pygame
import sys
from ui_modules.ui_input import Input
from ui_modules.ui_button import Button
#requirements ui_button, ui_input
class AskBox():
	def __init__(self,question="",title="",screen_res=()):
		MIDX = (screen_res[0]/2)-(450/2)
		MIDY = (screen_res[1]/2)-(250/2)
		self.text = ""
		self.question = question
		surface_temp = pygame.image.load("ui_modules/shapes/drawing_surface.png")
		self.drawing_surface = pygame.transform.scale(surface_temp, (450,250))
		headbar_temp = pygame.image.load("ui_modules/shapes/drawing_surface_head.png")
		self.headbar = pygame.transform.scale(headbar_temp, (450,50))
		self.used_font = pygame.font.SysFont(None,30)
		self.win_title = self.used_font.render(title,True,(255,255,255))
		self.new_font = pygame.font.SysFont(None,35)
		self.question_label = self.new_font.render(self.question,True,(255,255,255))
		self.input_box = Input(300,40,4,self.used_font,(255,255,255),(61, 61, 61),(28, 101, 156),(21, 70, 107),(MIDX+75,MIDY+120))
		self.submit_button = Button("Submit",pygame.font.SysFont(None,30),200,40,(MIDX+125,MIDY+190),(92, 91, 91),(56, 56, 56),(143, 141, 141),12)
		self.pressed = self.submit_button.pressed

	def render(self,screen,screen_res=()):
		for event in pygame.event.get():
			self.input_box.get_input(event)
		MIDX = (screen_res[0]/2)-(450/2)
		MIDY = (screen_res[1]/2)-(250/2)
		screen.blit(self.drawing_surface, (MIDX,MIDY))
		screen.blit(self.headbar, (MIDX,MIDY))
		screen.blit(self.win_title, (MIDX+165,MIDY+15))
		screen.blit(self.question_label, (MIDX+110,MIDY+70))
		self.input_box.render(screen)
		self.submit_button.draw(screen)
	def get_active(self):
		pressed = self.submit_button.check_click()
		return pressed
		
	def get_value(self):
		text = self.input_box.get_value()
		return text