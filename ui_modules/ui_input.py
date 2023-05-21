# This is the ui_input module it is made for the gui of the project manager
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

class Input:
	def __init__(self,width,height,border_width,font,text_color,input_color,border_color_active,border_color_passive,pos):
		#setting up core variables
		self.base_font = font
		self.user_text = ""
		self.text_color = text_color
		self.position = pos
		self.input_color = input_color
		self.border_color_active = border_color_active
		self.border_color_passive = border_color_passive
		self.border_width = border_width
		self.original_width = width
		self.current_color = border_color_passive
		self.active = False

		#defining surfaces
		self.text_surface = self.base_font.render(self.user_text,True,self.text_color)
		self.input_rect = pygame.Rect(self.position[0],self.position[1],width,height)
		self.border_rect = self.input_rect.copy()

	def render(self,screen):
		#changing width according to text length
		self.input_rect.w = self.original_width
		self.border_rect.w = self.original_width

		#changing color according to select status
		if self.active == True:
			self.current_color = self.border_color_active
		else:
			self.current_color = self.border_color_passive

		#rendering textbox to screen
		pygame.draw.rect(screen,self.input_color,self.input_rect)
		pygame.draw.rect(screen,self.current_color,self.border_rect,self.border_width)

		screen.blit(self.text_surface,(self.position[0]+10,self.position[1]+10))

	def get_input(self,event):
		#checking for input
		if event.type == pygame.MOUSEBUTTONDOWN:
			if self.input_rect.collidepoint(event.pos):
				self.active = True
			else:
				self.active = False

		if event.type == pygame.KEYDOWN:
			if self.active == True:
				if event.key == pygame.K_BACKSPACE:
					self.user_text = self.user_text[0:-1]
				else:
					if len(self.user_text) != (self.original_width/300)*26:
						self.user_text += event.unicode

		#updating text_surface
		self.text_surface = self.base_font.render(self.user_text,True,self.text_color)

	def get_value(self):
		return self.user_text