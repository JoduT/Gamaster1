from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '0'
import pygame

# Класс для описания платформы
class Platform(pygame.sprite.Sprite):
	def __init__(self, width, height):
		# Конструктор платформ
		super().__init__()
		self.image = pygame.image.load('pictures/platform_0.png')
		self.image = pygame.transform.scale(self.image, (200, 30))

		self.rect = self.image.get_rect()

class Coin(pygame.sprite.Sprite):
	def __init__(self, width, height):
		# Конструктор монет
		super().__init__()
		self.image = pygame.image.load('pictures/coin_0.png')
		self.image = pygame.transform.scale(self.image, (60, 60))

		self.rect = self.image.get_rect()

class Spikes(pygame.sprite.Sprite):
	def __init__(self, width, height):
		# Конструктор шипов
		super().__init__()
		self.image = pygame.image.load('pictures/Spikes_0.png')
		self.image = pygame.transform.scale(self.image, (60, 30))

		self.rect = self.image.get_rect()

class Batut(pygame.sprite.Sprite):
	def __init__(self, width, height):
		# Конструктор батутов
		super().__init__()
		self.image = pygame.image.load('pictures/batut_0.png')
		self.image = pygame.transform.scale(self.image, (50, 30))

		self.rect = self.image.get_rect()

class Portal(pygame.sprite.Sprite):
	def __init__(self, width, height):
		# Конструктор портала
		super().__init__()
		self.image = pygame.image.load('pictures/portal_0.png')
		self.image = pygame.transform.scale(self.image, (70, 100))

		self.rect = self.image.get_rect()
