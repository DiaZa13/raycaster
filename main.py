import pygame
from pygame import Color, image
import sys
from utils.windows.game import GameWindow
from utils.windows.start import StartWindow

TEXTURES = [image.load('utils/textures/wall1.png'),
            image.load('utils/textures/wall2.png'),
            image.load('utils/textures/wall3.png'),
            image.load('utils/textures/wall4.png'),
            image.load('utils/textures/wall5.png'),
            image.load('utils/textures/wall6.png')]

# Pygame setup
width = 1024
height = 500
pygame.init()
draw = pygame.draw
transform = pygame.transform
screen = pygame.display.set_mode((width, height),  pygame.DOUBLEBUF | pygame.HWACCEL)
screen.set_alpha(None)
# Window tittle
pygame.display.set_caption('Raycaster')
# Referencia al reloj de pygame
clock = pygame.time.Clock()
font = pygame.font.Font('utils/fonts/RoseRegular.ttf', 30)

''' START PAGE '''
start_page = StartWindow(screen, image, transform, width, height)

''' RAYCASTER '''
filename = './utils/maps/maze.txt'
game = GameWindow(screen, draw, transform, filename, clock, font)

# Validar en qué ventana está
playing = False
pause = False

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if not playing and not pause:
            playing = start_page.move_options(event, pygame)
        elif playing and not pause:
            game.move_options(event, pygame)
            game.floor_roof(Color('gray'), Color('khaki'), Color('wheat'))
            game.render(Color('navy'), TEXTURES)
            game.clock_update(60, Color('black'), Color('white'))
        else:
            ...

    pygame.display.update()


