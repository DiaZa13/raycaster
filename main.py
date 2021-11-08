import pygame
from pygame import Color, image, mixer
import sys
from utils.character.sprites import Sprites
from utils.windows.game import GameWindow
from utils.windows.start import StartWindow

L1_TEXTURES = [image.load('utils/textures/wall1.png'),
               image.load('utils/textures/wall2.png'),
               image.load('utils/textures/wall3.png'),
               image.load('utils/textures/wall4.png'),
               image.load('utils/textures/wall5.png'),
               image.load('utils/textures/wall6.png')]

L2_TEXTURES = [image.load('utils/textures/land2.png'),
               image.load('utils/textures/land5.png'),
               image.load('utils/textures/land7.png'),
               image.load('utils/textures/land8.png'),
               image.load('utils/textures/land9.png')]

L3_TEXTURES = [image.load('utils/textures/wall7.png'),
               image.load('utils/textures/wall9.png'),
               image.load('utils/textures/tools.png'),
               image.load('utils/textures/stall.png'),
               image.load('utils/textures/window2.png'),
               image.load('utils/textures/door1.png'),
               image.load('utils/textures/furnace.png')]

textures = [L1_TEXTURES, L2_TEXTURES, L3_TEXTURES]

L1_ENEMIES = [Sprites(300, 310, image.load('utils/sprites/enemy.png')),
              Sprites(100, 180, image.load('utils/sprites/enemy1.png')),
              Sprites(110, 290, image.load('utils/sprites/enemy2.png'))]

# Pygame setup
width = 700
height = 500
pygame.init()
draw = pygame.draw
transform = pygame.transform
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL)
screen.set_alpha(None)
# Window tittle
pygame.display.set_caption('Raycaster')
# Referencia al reloj de pygame
clock = pygame.time.Clock()

song = 'utils/music/nightmare.mp3'
start_page = StartWindow(screen, image, transform, width, height, song)

''' LEVEL1 '''
level1 = './utils/maps/maze.txt'
level2 = './utils/maps/level2.txt'
level3 = './utils/maps/level3.txt'
levels = ['./utils/maps/maze.txt', './utils/maps/level2.txt', './utils/maps/level3.txt']
game = GameWindow(screen, draw, transform, clock, image, L1_ENEMIES)

# Validar en qué ventana está
playing = False

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if not playing:
            if game.re_render:
                start_page = StartWindow(screen, image, transform, width, height, song)
                game.re_render = False
            playing = start_page.move_options(event, pygame)
        elif playing:
            game.floor_roof(Color('gray'), Color('black'), Color('wheat'))
            game.render(Color('navy'), Color('darkorchid'), textures[game.level], levels[game.level])
            playing, x, y = game.move_options(event, pygame)
            print(x, y)
            game.clock_update(60, Color('black'), Color('white'))

    pygame.display.update()
