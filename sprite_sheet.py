import pygame

class SpriteSheet():
	def __init__(self, image):
		self.sheet = image

	def get_image(self, frame, width, height, scale, colour, sheet_row = 0):
		image = pygame.Surface((width, height))
		image.blit(self.sheet, (0, 0), ((frame * width), sheet_row * height, width, height))
		image = pygame.transform.scale(image, (width * scale, height * scale))
		image.set_colorkey(colour)

		return image