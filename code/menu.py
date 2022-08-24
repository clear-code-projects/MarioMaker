import pygame
from pygame.math import Vector2 as vector
from pygame.image import load
from settings import *

class Menu:
	def __init__(self):

		# setup
		self.display_surface = pygame.display.get_surface()
		self.box_sprites = pygame.sprite.Group()

		self.create_data()
		self.create_buttons()

	def create_data(self):
		self.menu_surfs = {}
		for key, value in SURFACE_DATA.items():
			if not value['style'] in self.menu_surfs:
				self.menu_surfs[value['style']] = [(key,load(value['menu']))]
			else:
				self.menu_surfs[value['style']].append((key,load(value['menu'])))

	def create_buttons(self):

		# item buttons 
		main_size = 180
		self.main_rect = pygame.Rect(WINDOW_WIDTH - main_size - 6,WINDOW_HEIGHT - main_size - 6,main_size,main_size)

		# generic rect box
		self.generic_rect = pygame.Rect(self.main_rect.topleft,(self.main_rect.width * 0.48,self.main_rect.height * 0.48))

		# terrain box
		self.terrain_rect = self.generic_rect.copy()
		Button(self.terrain_rect, self.box_sprites, self.menu_surfs['terrain'])

		# coin box
		self.coin_rect = self.generic_rect.copy()
		self.coin_rect.topright = self.main_rect.topright
		Button(self.coin_rect, self.box_sprites, self.menu_surfs['static'])

		# palm box
		self.palm_rect = self.generic_rect.copy()
		self.palm_rect.bottomleft = self.main_rect.bottomleft
		Button(self.palm_rect, self.box_sprites, self.menu_surfs['palm_fg'], self.menu_surfs['palm_bg'])

		# enemies 
		self.enemy_rect = self.generic_rect.copy()
		self.enemy_rect.bottomright = self.main_rect.bottomright
		Button(self.enemy_rect, self.box_sprites, self.menu_surfs['enemy'])

	def check_mouse(self, pos, button):
		for sprite in self.box_sprites:
			if sprite.rect.collidepoint(pos):
				if button[1]: sprite.toggle_alt()
				if button[2]: sprite.switch()
				return sprite.get_id()

	def display(self):
		self.box_sprites.draw(self.display_surface)
		self.box_sprites.update()


class Button(pygame.sprite.Sprite):
	def __init__(self, rect,group, items, items_alt = None):

		# general
		super().__init__(group)
		self.image = pygame.Surface(rect.size)
		self.rect = rect

		# items 
		self.items = items
		self.index = 0
		self.rect_center = (self.rect.width / 2, self.rect.height / 2)

		# alternative items
		self.items_alt = items_alt
		self.alt_active = False

	def get_id(self):
		if not self.alt_active:
			return self.items[self.index][0]#, self.items[self.index][1]
		else:
			return self.items_alt[self.index][0]#, self.items_alt[self.index][1]

	def switch(self):
		self.index += 1
		self.index = 0 if self.index >= len(self.items) else self.index

		if self.items_alt:
			if self.index >= len(self.items_alt):
				self.index = 0

	def toggle_alt(self):
		if self.items_alt:
			self.alt_active = not self.alt_active

	def display_main(self):
		surf = self.items[self.index][1]
		rect = surf.get_rect(center = self.rect_center)
		self.image.blit(surf, rect)

	def display_alt(self):
		surf = self.items_alt[self.index][1]
		rect = surf.get_rect(center = self.rect_center)
		self.image.blit(surf, rect)

	def update(self):
		self.image.fill('black')
		if not self.alt_active:
			self.display_main()
		else:
			self.display_alt()