import pygame, sys
from pygame.math import Vector2 as vector
from pygame.image import load
from pygame.mouse import get_pos, get_pressed
from menu import Menu

from settings import *
from support import *

from debug import debug

class Editor:
	def __init__(self):
		
		# display
		self.display_surface = pygame.display.get_surface()
		self.image_data = {key: load(value['canvas']) for key, value in SURFACE_DATA.items()}

		# support line surf
		self.tile_line_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
		self.tile_line_surf.set_colorkey('green')
		self.tile_line_surf.set_alpha(30)

		# groups 
		self.canvas_tiles = CanvasGroup(self.image_data)
		self.canvas_objects = pygame.sprite.Group()

		# navigation
		self.origin = vector()
		self.pan_active = False
		self.pan_offset = vector()
		
		# selection
		self.selection_index = 0
		self.selected_pos = None
		self.object_drag_active = False

		# menu
		self.menu = Menu()
		
		# player 
		self.player = CanvasObject((200,WINDOW_HEIGHT / 2), self.image_data[0], 0, self.origin, self.canvas_objects)
		self.sky_handle = CanvasObject((WINDOW_WIDTH / 2,WINDOW_HEIGHT / 2), self.image_data[1], 1, self.origin, self.canvas_objects)
		self.create_grid()


	# support
	def draw_tile_lines(self):
		
		color = 'black'
		origin_offset = vector(
			x = self.origin.x - int(self.origin.x / TILE_SIZE) * TILE_SIZE, 
			y = self.origin.y - int(self.origin.y / TILE_SIZE) * TILE_SIZE)
		
		self.tile_line_surf.fill('green')
		
		for col in range(COLS + 1):
			x = origin_offset.x + col * TILE_SIZE
			pygame.draw.line(self.tile_line_surf, color, (x, 0),(x, WINDOW_HEIGHT))

		for row in range(ROWS + 1):
			y = origin_offset.y + row * TILE_SIZE
			pygame.draw.line(self.tile_line_surf, color, (0, y),(WINDOW_WIDTH, y))

		self.display_surface.blit(self.tile_line_surf,(0,0))

	def mouse_on_object(self):
		for sprite in self.canvas_objects:
			if sprite.rect.collidepoint(get_pos()):
				return sprite

	def get_cell_pos(self, mode = 'xy', pos = None): # should be more flexible to include mouse of obj
		
		if not pos:
			distance_to_origin = vector(pygame.mouse.get_pos()) - self.origin
		else:
			distance_to_origin = vector(pos) - self.origin


		col = distance_to_origin.x // TILE_SIZE
		row = distance_to_origin.y // TILE_SIZE

		x_pos = self.origin.x + col * TILE_SIZE
		y_pos = self.origin.y + row * TILE_SIZE
		
		if mode == 'grid': return col, row
		elif mode == 'xy': return x_pos, y_pos


	# input
	def event_loop(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			
			self.pan_input(event)
			self.menu_click(event)

			self.object_drag(event)
			self.canvas_delete(event)

	def canvas_left_click(self):
		if get_pressed()[0] and type(self.selection_index) == int and not self.menu.main_rect.collidepoint(get_pos()) and not self.mouse_on_object() and not self.object_drag_active:
				
			if SURFACE_DATA[self.selection_index]['type'] == 'tile':

				# get basic data 
				x, y = self.get_cell_pos('xy')
				
				# only update if changing cell
				if (x,y) != self.selected_pos:

					# info
					distance_to_origin = vector(x,y) - self.origin
					selected_tile = None
					cell = self.get_cell_pos('grid')
					
					# not tile yet 
					if cell not in [sprite.cell for sprite in self.canvas_tiles]:
						selected_tile = CanvasTile(pos = (x,y), cell = cell, tile_id = self.selection_index, distance_to_origin = distance_to_origin, group = self.canvas_tiles)

					# tile exists
					else:
						selected_tile = [sprite for sprite in self.canvas_tiles if sprite.cell == cell][0]
						selected_tile.add_id(self.selection_index)

					# check neighbors of all terrain tiles 
					if SURFACE_DATA[self.selection_index]['style'] in ('terrain', 'water') and selected_tile:
						nearby_tiles = [tile for tile in self.canvas_tiles if vector(tile.rect.center).distance_to(vector(selected_tile.rect.center)) < TILE_SIZE * 1.5 ]
						for tile in nearby_tiles:
							tile.check_neighbours()

					self.selected_pos = (x,y)

			else:
				CanvasObject(get_pos(), self.image_data[self.selection_index], self.selection_index, self.origin, self.canvas_objects)
			
			# self.create_grid()

	def menu_click(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN and self.menu.main_rect.collidepoint(pygame.mouse.get_pos()):
				self.selection_index = self.menu.check_mouse(get_pos(), get_pressed())

	def object_drag(self, event):
		# left click on object
		if event.type == pygame.MOUSEBUTTONDOWN and get_pressed()[0]:
			for sprite in self.canvas_objects:
				if sprite.rect.collidepoint(event.pos):
					sprite.selected = True
					sprite.mouse_offset = vector(pygame.mouse.get_pos()) - vector(sprite.rect.topleft)
					self.object_drag_active = True

		
		# if not pygame.mouse.get_pressed()[0]:
		if event.type == pygame.MOUSEBUTTONUP and any([sprite.selected for sprite in self.canvas_objects]):
			for sprite in self.canvas_objects:
				if sprite.selected:
					sprite.distance_to_origin = vector(sprite.rect.topleft) - self.origin
					sprite.selected = False
					self.object_drag_active = False
					self.create_grid()

	def canvas_delete(self, event):
		selected_sprite = self.mouse_on_object()
		pos = get_pos()

		if get_pressed()[2] and not self.menu.main_rect.collidepoint(pos):
			
			# delete object
			if selected_sprite:
				if selected_sprite.tile_id > 1:
					selected_sprite.kill()
				self.create_grid()
			
			# delete tile
			else:
				if len(self.canvas_tiles) > 0:
					for tile in self.canvas_tiles:
						if tile.rect.collidepoint(pos):
							tile.remove_tile(self.selection_index)
							self.create_grid()


	# navigation
	def pan_input(self,event):
			
		# middle mouse button pressed / released
		if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[1]:
			self.pan_active = True
			self.pan_offset = vector(pygame.mouse.get_pos()) - self.origin # get distance between mouse and origin
		if not pygame.mouse.get_pressed()[1]:
			self.pan_active = False

		# mouse wheel 
		if event.type == pygame.MOUSEWHEEL:
			if pygame.key.get_pressed()[pygame.K_LCTRL]: 
				self.origin.y -= event.y * 50
			else: 
				self.origin.x -= event.y * 50
			self.pan_active = True
			self.pan_offset = vector(pygame.mouse.get_pos()) - self.origin
	
	def pan_canvas(self):
		if self.pan_active:
			self.origin = vector(pygame.mouse.get_pos()) - self.pan_offset # move origin to mouse with offset

		# update all sprites 
			for sprite in self.canvas_tiles.sprites() + self.canvas_objects.sprites():
				sprite.pan_pos(self.origin)

	def image_preview(self):
		selected_sprite = self.mouse_on_object()

		# hover over object
		if selected_sprite:
			rect = selected_sprite.rect.inflate(10,10)
			r_size = 15
			r_color = 'black'
			r_width = 3

			# topleft
			pygame.draw.lines(self.display_surface, r_color,False, ((rect.left, rect.top + r_size),rect.topleft, (rect.left + r_size, rect.top)),r_width)
			
			# topright
			pygame.draw.lines(self.display_surface, r_color,False, ((rect.right - r_size, rect.top),rect.topright, (rect.right, rect.top + r_size)),r_width)

			# bottomleft
			pygame.draw.lines(self.display_surface, r_color,False, ((rect.left, rect.bottom - r_size),rect.bottomleft, (rect.left + r_size, rect.bottom)),r_width)
			
			# topright
			pygame.draw.lines(self.display_surface, r_color,False, ((rect.right - r_size, rect.bottom),rect.bottomright, (rect.right, rect.bottom - r_size)),r_width)
			

		# place things
		else:
			type_dict = {key: value['type'] for key, value in SURFACE_DATA.items()}
			if type_dict[self.selection_index] == 'tile':
				x,y = self.get_cell_pos()
				rect = pygame.Rect(x,y,TILE_SIZE, TILE_SIZE)
				self.display_surface.blit(self.image_data[self.selection_index],rect)
			else:
				rect = self.image_data[self.selection_index].get_rect(center = get_pos())
				self.display_surface.blit(self.image_data[self.selection_index],rect)
		

	# grid
	def convert_obj_to_tile(self):
		for tile in self.canvas_tiles:
			tile.objects = []
			tile.check_content()
		
		for sprite in self.canvas_objects:

			x,y = self.get_cell_pos('xy',sprite.rect.topleft)
			cell = self.get_cell_pos('grid', sprite.rect.topleft)
			distance_to_origin = vector(x,y) - self.origin
			
			# create new editorTile
			if cell not in [sprite.cell for sprite in self.canvas_tiles]:
				offset = vector(sprite.rect.x - x, sprite.rect.y - y)
				CanvasTile((x,y), cell, sprite.tile_id, distance_to_origin, self.canvas_tiles, offset)
			# add to existing tile
			else:
				cell = [sprite for sprite in self.canvas_tiles if sprite.cell == cell][0]
				offset = vector(sprite.rect.x - x, sprite.rect.y - y)
				cell.add_id(sprite.tile_id, offset)

	def create_grid(self):
		self.convert_obj_to_tile()
		if len(self.canvas_tiles):	
			
			# get topleft cell 
			top = sorted(self.canvas_tiles.sprites(), key =  lambda sprite: sprite.rect.y)[0]
			left = sorted(self.canvas_tiles.sprites(), key =  lambda sprite: sprite.rect.x)[0]
			
			# get bottomright cell
			right = sorted(self.canvas_tiles.sprites(), key =  lambda sprite: sprite.rect.x)[-1]
			bottom = sorted(self.canvas_tiles.sprites(), key =  lambda sprite: sprite.rect.y)[-1]

			# level dimensions
			level_width = (right.rect.right - left.rect.left) // TILE_SIZE
			level_height = (bottom.rect.bottom - top.rect.top) // TILE_SIZE
			# print(f'w: {level_width} h: {level_height}')

			# creating the grid
			self.grid = [[GridCell() for col in range(level_width)] for row in range(level_height)]

			# converting positions into a grid
			for row_index, row in enumerate(self.grid):
				for col_index, col in enumerate(row):
					x = left.rect.x + col_index * TILE_SIZE
					y = top.rect.y + row_index * TILE_SIZE
					for sprite in self.canvas_tiles:
						if sprite.rect.collidepoint((x,y)):
							self.grid[row_index][col_index].copy_ids(sprite)


	# sky
	def display_sky(self):
		y = self.sky_handle.rect.centery 
		self.display_surface.fill('#ddc6a1')

		# sea
		if y < WINDOW_HEIGHT:
			sea_rect = pygame.Rect(0,y,WINDOW_WIDTH,WINDOW_HEIGHT)
			pygame.draw.rect(self.display_surface,'#92a9ce',sea_rect)
		if y < 0:
			self.display_surface.fill('#92a9ce')

		# horizon
		pygame.draw.line(self.display_surface, 'white', (0,y), (WINDOW_WIDTH,y),5)

		if y > 20:
			horizon_rect1 = pygame.Rect(0,y - 10,WINDOW_WIDTH,10)
			horizon_rect2 = pygame.Rect(0,y - 16,WINDOW_WIDTH,4)
			horizon_rect3 = pygame.Rect(0,y - 20,WINDOW_WIDTH,2)
			pygame.draw.rect(self.display_surface, '#d1aa9d', horizon_rect1)
			pygame.draw.rect(self.display_surface, '#d1aa9d', horizon_rect2)
			pygame.draw.rect(self.display_surface, '#d1aa9d', horizon_rect3)

	# update
	def update(self, clock):
		self.display_surface.fill('white')
		self.display_sky()
		
		# input
		self.event_loop()
		self.canvas_left_click()

		# updating
		self.pan_canvas()
		self.canvas_objects.update()

		# drawing
		self.draw_tile_lines()
		# self.canvas_tiles.draw(self.display_surface)
		self.canvas_tiles.display_level()
		# self.canvas_objects.draw(self.display_surface)
		
		self.image_preview()

		for sprite in self.canvas_tiles:
			sprite.show_info()

		self.menu.display()
		debug(len(self.canvas_tiles))
		debug(int(clock.get_fps()), 30)

class CanvasGroup(pygame.sprite.Group):
	def __init__(self, image_data):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.image_data = image_data

		self.water_tiles = import_folder_dict('../graphics/terrain/water/')
		self.land_tiles = import_folder_dict('../graphics/terrain/land/')
		
	def display_level(self):

		for sprite in self:			
			if sprite.has_water:
				if sprite.water_top:
					self.display_surface.blit(self.water_tiles['water_bottom'], sprite.rect.topleft)
				else:
					self.display_surface.blit(self.water_tiles['water_top'], sprite.rect.topleft)

			if sprite.has_terrain:
				tile_name = ''.join(sprite.terrain_neighbors)
				if tile_name in self.land_tiles:
					self.display_surface.blit(self.land_tiles[tile_name], sprite.rect.topleft)
				else:
					self.display_surface.blit(self.land_tiles['X'], sprite.rect.topleft)

				# diagnostics
				if pygame.key.get_pressed()[pygame.K_SPACE]:
					self.display_surface.blit(sprite.image, sprite.rect.topleft)

			if sprite.static:
				self.display_surface.blit(self.image_data[sprite.coin], sprite.rect.topleft)

			if sprite.objects:
				for obj_data in sprite.objects:
					self.display_surface.blit(self.image_data[obj_data[0]],sprite.rect.topleft + obj_data[1])

class CanvasTile(pygame.sprite.Sprite):
	def __init__(self, pos, cell, tile_id, distance_to_origin, group, offset = vector()):
		super().__init__(group)

		# setup
		self.image = pygame.Surface((TILE_SIZE,TILE_SIZE))
		self.rect = self.image.get_rect(topleft = pos)

		# navigation
		self.font = pygame.font.Font(None, 16)
		self.distance_to_origin = distance_to_origin
		self.group = group
		self.cell = cell

		# terrain
		self.has_terrain = False
		self.terrain_neighbors = []
		
		
		# water
		self.has_water = False
		self.water_on_top = False
		
		# objects
		self.objects = []
		
		# coin / spikes
		self.static = None

		self.add_id(tile_id, offset = offset)

	def add_id(self, tile_id, offset = vector()):
		options = {key: value['style'] for key, value in SURFACE_DATA.items()}
		match options[tile_id]:
			case 'terrain': self.has_terrain = True
			case 'water':   self.has_water = True
			case 'static':  self.static = tile_id
			case _: # objects
				if (tile_id, offset) not in self.objects:
					self.objects.append((tile_id, offset)) 
	
	def remove_tile(self, tile_id):
		options = {key: value['style'] for key, value in SURFACE_DATA.items()}
		match options[tile_id]:
			case 'terrain': self.has_terrain = False
			case 'water':   self.has_water = False
			case 'static':  self.static = None
		self.check_content()

	def check_content(self):
		if not self.has_terrain and not self.has_water and not self.objects and not self.static:
			self.kill()

	def pan_pos(self, origin):
		self.rect.topleft = origin + self.distance_to_origin

	def check_neighbours(self):
		self.terrain_neighbors = []
		for key, pos in COLLISION_POINTS.items():
			point = self.rect.center + vector(pos)
			for tile in self.group:
				if tile.rect.collidepoint(point):

					# water 
					if key == 'A' and tile.has_water:
						self.water_top = True

					if tile.has_terrain:
						self.terrain_neighbors.append(key)

	def show_info(self):
		self.image.fill('black')
		
		# # terrain
		# tile_surf = self.font.render(f'{self.tile_ids}',True, 'White')
		# tile_rect = tile_surf.get_rect(topleft = (1,1))
		# self.image.blit(tile_surf, tile_rect)

		# # coin
		# coin_surf = self.font.render(f'{self.coin}',True, 'White')
		# coin_rect =	coin_surf.get_rect(topleft = tile_rect.bottomleft)
		# self.image.blit(coin_surf, coin_rect)

		# # object
		# # txt = f'{self.objects[0][0]},{self.objects[0][1].x},{self.objects[0][1].y}'
		# txt = f'{len(self.objects)}'
		# obj_surf = self.font.render(txt, True, 'White')
		# obj_rect = obj_surf.get_rect(topleft = coin_rect.bottomleft)
		# self.image.blit(obj_surf, obj_rect)

		# rect
		# txt_surf = self.font.render(f'{self.rect.topleft}', True, 'White')
		# txt_rect = txt_surf.get_rect(topleft = (1,1))
		# self.image.blit(txt_surf, txt_rect)

		# neighbors
		txt_surf = self.font.render(f'{list(self.terrain_neighbors)[0:3]}', True, 'White')
		txt_rect = txt_surf.get_rect(topleft = (1,1))
		self.image.blit(txt_surf, txt_rect)

		txt_surf2 = self.font.render(f'{list(self.terrain_neighbors)[3:]}', True, 'White')
		txt_rect2 = txt_surf2.get_rect(topleft = txt_rect.bottomleft)
		self.image.blit(txt_surf2, txt_rect2)

class CanvasObject(pygame.sprite.Sprite):
	def __init__(self, pos, surf, tile_id, origin, group):
		super().__init__(group)

		#sprite setup
		self.image = surf
		self.rect = self.image.get_rect(center = pos)

		self.tile_id = tile_id
		
		# drag
		self.selected = False
		self.mouse_offset = vector()

		# pan
		self.distance_to_origin = vector(self.rect.topleft) - origin

	def pan_pos(self, origin):
		self.rect.topleft = origin + self.distance_to_origin

	def update(self):
		if self.selected:
			self.rect.topleft = pygame.mouse.get_pos() - self.mouse_offset

class GridCell:
	def __init__(self):
		self.tile_ids = []
		self.objects = []
		self.coin = None

	def copy_ids(self, tile):
		self.has_terrain = tile.has_terrain
		self.terrain_neighbors = tile.terrain_neighbors

		self.has_water = tile.has_water
		self.water_on_top = tile.water_on_top

		self.static = tile.static
		self.objects = tile.objects

	def __repr__(self):
		return 'Grid'
		# return f'Grid({self.tile_ids}, {self.objects}, {self.coin})'