# general setup
TILE_SIZE = 64
COLS = 20
ROWS = 12
WINDOW_WIDTH = COLS * TILE_SIZE
WINDOW_HEIGHT = ROWS * TILE_SIZE

# editor graphics 
SURFACE_DATA = {
	0: {'style': 'player', 'type': 'object', 'canvas': '../graphics/menu/player/idle.png', 'menu': '../graphics/menu/player/idle.png'},
	1: {'style': 'sky', 'type': 'object', 'canvas': '../graphics/menu/cloud/cloud.png', 'menu': '../graphics/menu/cloud/cloud.png'},
	
	2: {'style': 'terrain', 'type': 'tile', 'canvas': '../graphics/menu/terrain/land.png',  'menu': '../graphics/menu/terrain/land.png'},
	3: {'style': 'water',   'type': 'tile', 'canvas': '../graphics/menu/terrain/water.png', 'menu': '../graphics/menu/terrain/water.png'},
	
	4: {'style': 'static', 'type': 'tile', 'canvas': '../graphics/menu/items/gold.png',     'menu': '../graphics/menu/items/gold.png'},
	5: {'style': 'static', 'type': 'tile', 'canvas': '../graphics/menu/items/silver.png',   'menu': '../graphics/menu/items/silver.png'},
	6: {'style': 'static', 'type': 'tile', 'canvas': '../graphics/menu/items/diamond.png',  'menu': '../graphics/menu/items/diamond.png'},
	7: {'style': 'static', 'type': 'tile', 'canvas': '../graphics/menu/enemies/spikes.png', 'menu': '../graphics/menu/enemies/spikes.png'},

	8:  {'style': 'enemy', 'type': 'object', 'canvas': '../graphics/menu/enemies/tooth.png',       'menu': '../graphics/menu/enemies/tooth.png'},
	9:  {'style': 'enemy', 'type': 'object', 'canvas': '../graphics/menu/enemies/shell_left.png',  'menu': '../graphics/menu/enemies/shell_left.png'},
	10: {'style': 'enemy', 'type': 'object', 'canvas': '../graphics/menu/enemies/shell_right.png', 'menu': '../graphics/menu/enemies/shell_right.png'},
	
	11: {'style': 'palm_fg', 'type': 'object', 'canvas': '../graphics/palm/small_fg.png', 'menu': '../graphics/menu/palm/small_fg.png'},
	12: {'style': 'palm_fg', 'type': 'object', 'canvas': '../graphics/palm/large_fg.png', 'menu': '../graphics/menu/palm/large_fg.png'},
	13: {'style': 'palm_fg', 'type': 'object', 'canvas': '../graphics/menu/palm/left_fg.png',  'menu': '../graphics/menu/palm/left_fg.png'},
	14: {'style': 'palm_fg', 'type': 'object', 'canvas': '../graphics/menu/palm/right_fg.png', 'menu': '../graphics/menu/palm/right_fg.png'},

	15: {'style': 'palm_bg', 'type': 'object', 'canvas': '../graphics/palm/small_fg.png',      'menu': '../graphics/menu/palm/small_bg.png'},
	16: {'style': 'palm_bg', 'type': 'object', 'canvas': '../graphics/palm/large_fg.png',      'menu': '../graphics/menu/palm/large_bg.png'},
	17: {'style': 'palm_bg', 'type': 'object', 'canvas': '../graphics/menu/palm/left_bg.png',  'menu': '../graphics/menu/palm/left_bg.png'},
	18: {'style': 'palm_bg', 'type': 'object', 'canvas': '../graphics/menu/palm/right_bg.png', 'menu': '../graphics/menu/palm/right_bg.png'},

}

# sprite collisions
COLLISION_POINTS = {
	'A': (0,-TILE_SIZE),
	'B': (TILE_SIZE,-TILE_SIZE),
	'C': (TILE_SIZE,0),
	'D': (TILE_SIZE,TILE_SIZE),
	'E': (0,TILE_SIZE),
	'F': (-TILE_SIZE, TILE_SIZE),
	'G': (-TILE_SIZE, 0),
	'H': (-TILE_SIZE, -TILE_SIZE),
}