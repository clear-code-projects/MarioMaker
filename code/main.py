import pygame, sys
from settings import *
from editor import Editor
from debug import debug

class Main:
	def __init__(self):
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		self.clock = pygame.time.Clock()
		self.editor = Editor()

	def run(self):
		while True:
			self.editor.update(self.clock)
			pygame.display.update()
			self.clock.tick()

			# `pygame.display.set_caption(f'{int(self.clock.get_fps())}')
 
if __name__ == '__main__':
	main = Main()
	main.run() 