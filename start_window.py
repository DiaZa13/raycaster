import pygame
from pygame import Color
import sys
import os
from utils.UI.text import Text

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
maze_pos = (20, 2 / 4 * height)
Text(screen, font, 'MAZE', maze_pos, Color('black'))
camping_pos = (20, height - 25)
Text(screen, font, 'CAMPING', maze_pos, Color('black'))

# Menu de opciones
x = width - int(1 / 4 * width) - 50
menu_bck = pygame.Surface((int(1 / 4 * width), int(3 / 4 * height)), pygame.SRCALPHA)
menu_bck.fill((229, 236, 231, 102))
screen.blit(menu_bck, (x, 0))

# Opciones
font = pygame.font.Font('utils/fonts/Pixel.ttf', 50)
hover_font = pygame.font.Font('utils/fonts/Pixel.ttf', 70)
start_pos = (x + 70, int(1 / 2 * height) - 80)
start = Text(screen, font, 'PLAY', start_pos, Color('black'), Color('navy'), hover_font)
exit_pos = (x + 70, int(1 / 2 * height))
exit = Text(screen, font, 'EXIT', exit_pos, Color('black'), Color('navy'), hover_font)

# TODO Agregar flechita para que se vea más cool
# pygame.draw.polygon(screen, (0, 0, 0), ((0, 100), (0, 200), (200, 200), (200, 300), (300, 150), (200, 0), (200, 100)))
while 1:
    time_delta = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                start._hover = True
                exit._hover = False
            elif event.key == pygame.K_DOWN:
                start._hover = False
                exit._hover = True
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                # TODO cambiar de pestaña
                if start._hover:
                    ...
                elif exit._hover:
                    sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            if start.rect.collidepoint(event.pos):
                start._hover = True
                exit._hover = False
            if exit.rect.collidepoint(event.pos):
                start._hover = False
                exit._hover = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # TODO condicionar si hace click a play
            if start.rect.collidepoint(event.pos):
                sys.exit()
            if exit.rect.collidepoint(event.pos):
                sys.exit()

    start.draw_text()
    exit.draw_text()

    pygame.display.update()


