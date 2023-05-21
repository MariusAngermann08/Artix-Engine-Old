# This is the ui_button module it is made for the gui of the project manager
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

class Button:
    def __init__(self,text,font,width,height,pos,surf_color,bottom_color,hover_color,border_radius):
        #Core attributes
        self.pressed = False
        self.original_pos = pos
        
        #style
        self.border_radius = border_radius
        self.hover_color = hover_color
        self.core_color = surf_color
        self.elevation = 6
        self.dynamic_elevation = self.elevation

        #top rectangle
        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = surf_color

        #bottom rectangle
        self.bottom_rect = pygame.Rect(pos,(width,self.elevation))
        self.bottom_color = bottom_color

        #text
        self.text_surf = font.render(text,True,(255,255,255))
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def draw(self,screen):
        #elevation logic
        self.top_rect.y = self.original_pos[1] - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        #drawing button
        pygame.draw.rect(screen,self.bottom_color,self.bottom_rect, border_radius = self.border_radius)
        pygame.draw.rect(screen,self.top_color,self.top_rect, border_radius = self.border_radius)
        screen.blit(self.text_surf,self.text_rect)

        self.check_click()

    def check_click(self):
        #checking for click
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = self.hover_color
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True
            else:
                if self.pressed == True:
                    self.dynamic_elevation = self.elevation
                    self.pressed = False
                    return True
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = self.core_color

    def move(self, vector):
        self.original_pos = (self.original_pos[0] + vector[0], self.original_pos[1] + vector[1])
        self.top_rect = pygame.Rect(self.original_pos, (self.top_rect.width, self.top_rect.height))
        self.bottom_rect = pygame.Rect(self.original_pos, (self.bottom_rect.width, self.elevation))
        self.text_rect.center = self.top_rect.center
