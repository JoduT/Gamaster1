import os
import time
import random
from classes import Platform, Coin, Spikes, Batut, Portal
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '0'
import pygame

# Переменные для установки ширины и высоты окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

running = True #значение без которого не будет ничего работать

# Подключение фото для заднего фона
# Здесь лишь создание переменной, вывод заднего фона ниже в коде
bg = pygame.image.load('pictures/bg_0.jpg')

level_number = random.randint(1, 3)

# Класс, описывающий поведение главного игрока
class Player(pygame.sprite.Sprite):
	# Изначально игрок смотрит вправо, поэтому эта переменная True
	right = True

	# Методы
	def __init__(self):
		# Стандартный конструктор класса
		# Нужно ещё вызывать конструктор родительского класса
		super().__init__()

		# Создаем изображение для игрока
		# Изображение находится в этой же папке проекта
		self.image = pygame.image.load('pictures/idle_0.png')
		self.image = pygame.transform.scale(self.image, (42, 62))

		# Установите ссылку на изображение прямоугольника
		self.rect = self.image.get_rect()

		# Задаем вектор скорости игрока
		self.change_x = 0
		self.change_y = 0

	def update(self):
		# В этой функции мы передвигаем игрока
		# Сперва устанавливаем для него гравитацию
		self.calc_grav()

		# Передвигаем его на право/лево
		# change_x будет меняться позже при нажатии на стрелочки клавиатуры
		self.rect.x += self.change_x

		# Следим ударяем ли мы какой-то другой объект, платформы, например
		block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
		coin_hit_list = pygame.sprite.spritecollide(self, self.level.coin_list, False)
		spikes_hit_list = pygame.sprite.spritecollide(self, self.level.spikes_list, False)
		batut_hit_list = pygame.sprite.spritecollide(self, self.level.batut_list, False)
		teleport_hit_list = pygame.sprite.spritecollide(self, self.level.portal_list, False)

		# Перебираем все возможные объекты, с которыми могли бы столкнуться
		for block in block_hit_list: #соприкосновения с платформами
			if self.change_x > 0:
				self.rect.right = block.rect.left
			elif self.change_x < 0:
				self.rect.left = block.rect.right

		for batut in batut_hit_list: #соприкосновения с батутами
			if self.change_x > 0:
				if self.change_y >= 0:
					self.rect.right = batut.rect.left
			elif self.change_x < 0:
				if self.change_y >= 0:
					self.rect.left = batut.rect.right

		for coin in coin_hit_list: #соприкосновения с монетами
			if self.change_x > 0:
				current_level.destroy_coin(coin)
			elif self.change_x < 0:
				current_level.destroy_coin(coin)

		for spike in spikes_hit_list: #соприкосновения с шипами
			if self.change_x > 0:
				current_level.death()
			elif self.change_x < 0:
				current_level.death()

		for teleport in teleport_hit_list: #соприкосновения с телепортами
			if self.change_x > 0:
				current_level.teleport()
			elif self.change_x < 0:
				current_level.teleport()

		# Передвигаемся вверх/вниз
		self.rect.y += self.change_y

		# То же самое, вот только уже для вверх/вниз. Эту часть нельзя убрать, будет
		block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
		coin_hit_list = pygame.sprite.spritecollide(self, self.level.coin_list, False)
		spikes_hit_list = pygame.sprite.spritecollide(self, self.level.spikes_list, False)
		batut_hit_list = pygame.sprite.spritecollide(self, self.level.batut_list, False)
		teleport_hit_list = pygame.sprite.spritecollide(self, self.level.portal_list, False)

		for block in block_hit_list: #соприкосновения с платформами
			if self.change_y > 0:
				self.rect.bottom = block.rect.top
				self.change_y = 0
			elif self.change_y < 0:
				self.rect.top = block.rect.bottom
				self.change_y = 0

		for teleport in teleport_hit_list: #соприкосновения с телепортами
			if self.change_y > 0:
				current_level.teleport()
			elif self.change_y < 0:
				current_level.teleport()

		for coin in coin_hit_list: #соприкосновения с монетами
			if self.change_y > 0:
				current_level.destroy_coin(coin)
			elif self.change_y < 0:
				current_level.destroy_coin(coin)

		for batut in batut_hit_list: #соприкосновения с батутами
			if self.change_y >= 0:
				current_level.jump_batut()
			elif self.change_y < 0:
				if self.rect.top >= batut.rect.bottom:
					self.rect.top = batut.rect.bottom
					self.change_y = 0

		for spike in spikes_hit_list: #соприкосновения с шипами
			if self.change_y > 0:
				current_level.death()
			elif self.change_y < 0:
				current_level.death()

	def calc_grav(self):
		# Здесь мы вычисляем как быстро объект будет
		# падать на землю под действием гравитации
		if self.change_y == 0:
			self.change_y = 1
		else:
			self.change_y += 0.80

		# Если уже на земле, то ставим позицию Y как 0
		if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
			self.change_y = 20
			self.rect.y = SCREEN_HEIGHT - self.rect.height

	def jump(self, jump_force):
		# Обработка прыжка
		# Нам нужно проверять здесь, контактируем ли мы с чем-либо
		# или другими словами, не находимся ли мы в полете.
		# Для этого опускаемся на 1 единицу, проверим соприкосновение и далее поднимаемся обратно
		self.rect.y += 1
		platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
		batut_hit_list = pygame.sprite.spritecollide(self, self.level.batut_list, False)
		self.rect.y -= 1

		# Если все в порядке, прыгаем вверх
		if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT or len(batut_hit_list) > 0:
			if jump_force == None:
				self.change_y = -17
			else:
				self.change_y = -jump_force

	# Передвижение игрока
	def go_left(self):
		# Сами функции будут вызваны позже из основного цикла
		self.change_x = -8 # Двигаем игрока по Х
		if(self.right): # Проверяем куда он смотрит и если что, то переворачиваем его
			self.flip()
			self.right = False

	def go_right(self):
		# то же самое, но вправо
		self.change_x = 8
		if (not self.right):
			self.flip()
			self.right = True

	def stop(self):
		# вызываем этот метод, когда не нажимаем на клавиши
		self.change_x = 0

	def flip(self):
		# переворот игрока (зеркальное отражение)
		self.image = pygame.transform.flip(self.image, True, False)

player = Player()

# Класс для расстановки платформ на сцене
class Level(object):
	global current_level, jump_force
	def __init__(self, player):
		# Создаем группу спрайтов (поместим платформы различные сюда)
		self.platform_list = pygame.sprite.Group()
		self.coin_list = pygame.sprite.Group()
		self.spikes_list = pygame.sprite.Group()
		self.batut_list = pygame.sprite.Group()
		self.portal_list = pygame.sprite.Group()
		# Ссылка на основного игрока
		self.player = player

	# Чтобы все рисовалось, то нужно обновлять экран
	# При вызове этого метода обновление будет происходить
	def update(self):
		self.platform_list.update()
		self.coin_list.update()
		self.spikes_list.update()
		self.batut_list.update()
		self.portal_list.update()
	# Метод для рисования объектов на сцене
	def draw(self, screen):
		# Рисуем задний фон
		screen.blit(bg, (0, 0))

		# Рисуем все платформы из группы спрайтов
		self.platform_list.draw(screen)
		self.coin_list.draw(screen)
		self.spikes_list.draw(screen)
		self.batut_list.draw(screen)
		self.portal_list.draw(screen)

	def destroy_coin(self, coin): #действие монетки
		self.coin_list.remove(coin)

	def death(self): #действие шипа
		time.sleep(0.5)
		main(level_number)

	def jump_batut(self):	#действие батута
		player.jump(25)

	def teleport(self):	#действие портала
		if len(self.coin_list) == 0:
			pygame.quit()
			os.system('python my_part (2).py')
		else:
			return

# Класс, что описывает где будут находиться все платформы, шипы, батуты, монетки, телепорты и т.д
# на определенном уровне игры
class Level_01(Level):
	def __init__(self, player):
		# Вызываем родительский конструктор
		Level.__init__(self, player)
		# Массив с данными про платформы. Данные в таком формате:
		# [ширина, высота, x и y позиция]
		level = [
			[110, 32, 530, 470],#координаты платформ на уровне
			[110, 32, 120, 400],
			[110, 32, 600, 300],
			[110, 32, 0, 120],
			[110, 32, -10, 570],
			[110, 32, 163, 570],
			[110, 32, 330, 570],
			[110, 32, 330+165, 570],
			[110, 32, 330+165+165, 570]
		]
		teleports = [	#координаты телепортов на уровне
			[64, 32, 5, 25]
		]
		batuts = [	#координаты батутов на уровне
			[32, 32, 250, 370]
		]
		coins = [	#координаты монеток на уровне
			[32, 32, 530, 410],
			[32, 32, 190, 340],
			[32, 32, 620, 240],
			[32, 32, 400, 80],
		]
		spikes = [	#координаты шипов на уровне
			[32, 32, 625, 440],
			[32, 32, 130, 370],
			[32, 32, 675, 270]
		]

		# Перебираем массив и добавляем каждую платформу в группу спрайтов - platform_list, coin_list,
		# spikes_list, batut_list, portal_list
		for platform in level:  #платформы на уровне 01
			block = Platform(platform[0], platform[1])
			block.rect.x = platform[2]
			block.rect.y = platform[3]
			block.player = self.player
			self.platform_list.add(block)

		for coin in coins:	#монетки на уровне
			monetka = Coin(coin[0], coin[1])
			monetka.rect.x = coin[2]
			monetka.rect.y = coin[3]
			monetka.player = self.player
			self.coin_list.add(monetka)

		for spike in spikes:	#шипы на уровне
			iron_spike = Spikes(spike[0], spike[1])
			iron_spike.rect.x = spike[2]
			iron_spike.rect.y = spike[3]
			iron_spike.player = self.player
			self.spikes_list.add(iron_spike)

		for batut in batuts:	#батуты на уровне
			prujina = Batut(batut[0], batut[1])
			prujina.rect.x = batut[2]
			prujina.rect.y = batut[3]
			prujina.player = self.player
			self.batut_list.add(prujina)

		for teleport in teleports:	#телепорты на уровне
			portal = Portal(teleport[0], teleport[1])
			portal.rect.x = teleport[2]
			portal.rect.y = teleport[3]
			portal.player = self.player
			self.portal_list.add(portal)

class Level_02(Level):
	def __init__(self, player):
		Level.__init__(self, player)
		level = [
			[110, 32, 760, 100],
			[110, 32, 580, 100],
			[110, 32, 540, 210],
			[110, 32, 540, 330],
			[110, 32, 170, 100],
			[110, 32, -10, 570], #1111
			[110, 32, 163, 570],
			[110, 32, 330, 570],
			[110, 32, 495, 570],
			[110, 32, 660, 570]
		]
		teleports = [
			[64, 32, 740, 125]
		]
		batuts = [
			[32, 32, 400, 540],
			[32, 32, 750, 540]
		]
		coins = [
			[64, 32, 720, 45],
			[32, 32, 615, 155],
			[32, 32, 615, 275],
			[110, 32, 70, 150],
			[110, 32, 70, 210],
			[110, 32, 70, 270],
			[110, 32, 70, 330],
		]
		spikes = [
			[32, 32, 590, 70],
			[32, 32, 670, 180],
			[32, 32, 670, 300],
		]
		for platform in level:
			block = Platform(platform[0], platform[1])
			block.rect.x = platform[2]
			block.rect.y = platform[3]
			block.player = self.player
			self.platform_list.add(block)

		for coin in coins:
			monetka = Coin(coin[0], coin[1])
			monetka.rect.x = coin[2]
			monetka.rect.y = coin[3]
			monetka.player = self.player
			self.coin_list.add(monetka)

		for spike in spikes:
			iron_spike = Spikes(spike[0], spike[1])
			iron_spike.rect.x = spike[2]
			iron_spike.rect.y = spike[3]
			iron_spike.player = self.player
			self.spikes_list.add(iron_spike)

		for batut in batuts:
			prujina = Batut(batut[0], batut[1])
			prujina.rect.x = batut[2]
			prujina.rect.y = batut[3]
			prujina.player = self.player
			self.batut_list.add(prujina)

		for teleport in teleports:
			portal = Portal(teleport[0], teleport[1])
			portal.rect.x = teleport[2]
			portal.rect.y = teleport[3]
			portal.player = self.player
			self.portal_list.add(portal)

class Level_03(Level):
	def __init__(self, player):
		Level.__init__(self, player)
		level = [
			[110, 32, -10, 570],#первый уровень
			[110, 32, 163, 570],
			[110, 32, 330, 570],
			[110, 32, 495, 570],
			[110, 32, 660, 570],
			[110, 32, -10, 440],#второй уровень
			[110, 32, 163, 440],
			[110, 32, 330, 440],
			[110, 32, 495, 440],
			#[110, 32, 660, 420],
			#[110, 32, -10, 250],#третий уровень
			[110, 32, 163, 250],
			[110, 32, 330, 250],
			[110, 32, 495, 250],
			[110, 32, 660, 250],
			[110, 32, -10, 70],#четвертый уровень
			[110, 32, 163, 70],
			#[110, 32, 330, 70],
			[110, 32, 495, 70],
			[110, 32, 660, 70],
		]
		teleports = [
			[110, 32, 10, -20],
		]
		batuts = [
			[110, 32, 10, 410],
		]
		coins = [
			[110, 32, 0, 515],
			[110, 32, 400, 385],
			[110, 32, 350, 385],
			[110, 32, 5, 300],
			[110, 32, 5, 240],
			[110, 32, 5, 180],
			[110, 32, 5, 120],
			[110, 32, 740, 195],
			[110, 32, 740, 15],
		]
		spikes = [
			[110, 32, 460, 410],
			[110, 32, 650, 220],
		]
		for platform in level:
			block = Platform(platform[0], platform[1])
			block.rect.x = platform[2]
			block.rect.y = platform[3]
			block.player = self.player
			self.platform_list.add(block)

		for coin in coins:
			monetka = Coin(coin[0], coin[1])
			monetka.rect.x = coin[2]
			monetka.rect.y = coin[3]
			monetka.player = self.player
			self.coin_list.add(monetka)

		for spike in spikes:
			iron_spike = Spikes(spike[0], spike[1])
			iron_spike.rect.x = spike[2]
			iron_spike.rect.y = spike[3]
			iron_spike.player = self.player
			self.spikes_list.add(iron_spike)

		for batut in batuts:
			prujina = Batut(batut[0], batut[1])
			prujina.rect.x = batut[2]
			prujina.rect.y = batut[3]
			prujina.player = self.player
			self.batut_list.add(prujina)

		for teleport in teleports:
			portal = Portal(teleport[0], teleport[1])
			portal.rect.x = teleport[2]
			portal.rect.y = teleport[3]
			portal.player = self.player
			self.portal_list.add(portal)

# Основная функция программы
def main(level_number):
	global level_list, current_level
	# Инициализация
	pygame.init()

	# Установка высоты и ширины
	size = [SCREEN_WIDTH, SCREEN_HEIGHT]
	screen = pygame.display.set_mode(size)

	# Название игры
	pygame.display.set_caption("Платформер")

	# Создаем все уровни
	level_list = [Level_01(player), Level_02(player), Level_03(player)]
	current_level = level_list[level_number - 1]

	active_sprite_list = pygame.sprite.Group()
	player.level = current_level

	player.rect.x = 340
	player.rect.y = SCREEN_HEIGHT - player.rect.height
	active_sprite_list.add(player)

	# Цикл будет до тех пор, пока пользователь не нажмет кнопку закрытия
	done = False

	# Используется для управления скоростью обновления экрана
	clock = pygame.time.Clock()

	# Основной цикл программы
	while not done:
		# Отслеживание действий
		for event in pygame.event.get():
			#global level_number_n
			if event.type == pygame.QUIT: # Если закрыл программу, то останавливаем цикл
				done = True

			# Если нажали на стрелки клавиатуры, то двигаем объект
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT: #бинды кнопок wasd и space
					player.go_left()
				if event.key == pygame.K_RIGHT:
					player.go_right()
				if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
					player.jump(None)
				# if event.key == pygame.K_1:  Что-то вроде читов, если убрать комментарии, то на кнопки 1-2-3 можно будет переключать уровни
				# 	main(1)
				# if event.key == pygame.K_2:
				# 	main(2)
				# if event.key == pygame.K_3:
				# 	main(3)

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT and player.change_x < 0: #останавливаемся в случае отжатия кнопок a и s
					player.stop()
				if event.key == pygame.K_RIGHT and player.change_x > 0:
					player.stop()

		# Обновляем игрока
		active_sprite_list.update()

		# Обновляем объекты на сцене
		current_level.update()

		# Если игрок приблизится к правой стороне, то дальше его не двигаем
		if player.rect.right > SCREEN_WIDTH:
			player.rect.right = SCREEN_WIDTH

		# Если игрок приблизится к левой стороне, то дальше его не двигаем
		if player.rect.left < 0:
			player.rect.left = 0

		# Рисуем объекты на окне
		current_level.draw(screen)
		active_sprite_list.draw(screen)

		# Устанавливаем количество фреймов (по идее аналог FPS)
		clock.tick(60)

		# Обновляем экран после рисования объектов
		pygame.display.flip()
	# Корректное закрытие программы
	pygame.quit()

#if running == True:
	#main(level_number)