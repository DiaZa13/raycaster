import pygame
from pygame import Color
import sys
import os

width = 1024
height = 500
pygame.init()
pygame.display.set_caption('Quick Start')
screen = pygame.display.set_mode((width, height))

# Imagen de fondo
background = pygame.image.load(os.path.join('utils/textures', 'night.png'))
background = pygame.transform.scale(background, (width, height))
screen.blit(background, [0, 0])
clock = pygame.time.Clock()

# Titulo
font = pygame.font.Font('utils/fonts/Pixel.ttf', 120)
title_a = 'MAZE'
title_b = 'CAMPING'
game_title_a = font.render(title_a, False, Color('white'))
screen.blit(game_title_a, (20, 2 / 4 * height))
game_title_b = font.render(title_b, False, Color('white'))
t_y = height - game_title_b.get_height() - 25
screen.blit(game_title_b, (20, t_y))

# Menu de opciones
x = width - int(1/4 * width) - 25
pygame.draw.rect(screen, Color('ivory'), (x, 0, int(1/4 * width), int(3/4 * height)))

while 1:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    pygame.display.update()
