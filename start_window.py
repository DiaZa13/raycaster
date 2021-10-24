import pygame
from pygame import Color, image
import sys
import os
from utils.UI.text import Text
from raycasterb import Raycaster
import math

COLORS = [Color('coral'),
          Color('lavenderblush4'),
          Color('lightskyblue'),
          Color('bisque'),
          Color('blueviolet')]

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
pygame.display.set_caption('Quick Start')
screen = pygame.display.set_mode((width, height),  pygame.DOUBLEBUF | pygame.HWACCEL)
screen.set_alpha(None)
# Window tittle
pygame.display.set_caption('Raycaster')

''' START PAGE '''
# Imagen de fondo
background = pygame.image.load(os.path.join('utils/textures', 'night.png'))
background = pygame.transform.scale(background, (width, height))
screen.blit(background, [0, 0])

# Titulo
font = pygame.font.Font('utils/fonts/Pixel.ttf', 120)
maze_pos = (20, 2 / 4 * height)
maze = Text(screen, font, 'MAZE', maze_pos, Color('white'))
camping_pos = (20, height - 25 - maze.rect[3])
Text(screen, font, 'CAMPING', camping_pos, Color('white'))

# Menu de opciones
x = width - int(1 / 4 * width) - 130
menu_bck = pygame.Surface((int(1 / 3 * width), int(6 / 7 * height)), pygame.SRCALPHA)
menu_bck.fill((229, 236, 231, 102))
screen.blit(menu_bck, (x, 0))

# Logo
logo = pygame.image.load(os.path.join('utils/textures', 'logo2.png'))
logo = pygame.transform.scale(logo, (180, 150))
screen.blit(logo, [x + 80, 15])

# Opciones
font = pygame.font.Font('utils/fonts/Pixel.ttf', 70)
hover_font = pygame.font.Font('utils/fonts/Pixel.ttf', 70)
start_pos = (x + 90, int(1 / 2 * height) - 40)
start = Text(screen, font, 'PLAY', start_pos, Color('black'), Color('chartreuse'), hover_font)
start._hover = True
exit_pos = (x + 90, int(1 / 2 * height) + 60)
exit = Text(screen, font, 'EXIT', exit_pos, Color('black'), Color('chartreuse'), hover_font)

''' RAYCASTER '''
caster = Raycaster(screen, draw, transform)
caster.loadMap('./utils/maps/maze.txt')

# Referencia al reloj de pygame
clock = pygame.time.Clock()
font = pygame.font.Font('utils/fonts/RoseRegular.ttf', 30)

''' PAUSE MENU '''
# x = width - int(1 / 4 * width) - 50
# menu_bck = pygame.Surface((int(1 / 4 * width), int(3 / 4 * height)), pygame.SRCALPHA)
# menu_bck.fill((229, 236, 231, 102))
# screen.blit(menu_bck, (x, 0))

def updateFps():
    fps = str(int(clock.get_fps()))
    fps = font.render(' ' + fps, False, Color('white'))
    return fps

# Validar en qué ventana está
playing = False

# TODO Agregar flechita para que se vea más cool
# pygame.draw.polygon(screen, (0, 0, 0), ((0, 100), (0, 200), (200, 200), (200, 300), (300, 150), (200, 0), (200, 100)))
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if not playing:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    start._hover = True
                    exit._hover = False
                elif event.key == pygame.K_DOWN:
                    start._hover = False
                    exit._hover = True
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    if start._hover:
                        playing = True
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
                    playing = True
                if exit.rect.collidepoint(event.pos):
                    sys.exit()

            start.draw_text()
            exit.draw_text()
        else:
            if event.type == pygame.KEYDOWN:
                x = caster.player['x']
                y = caster.player['y']
                forward = caster.player['angle'] * math.pi / 180
                right = (caster.player['angle'] + 90) * math.pi / 180
                # Revisar que el evento se activo por la llave
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key == pygame.K_w or event.key == pygame.K_RIGHT:
                    # Para poder moverme con respecto al ángulo del jugador
                    x += math.cos(forward) * caster.step_size
                    y += math.sin(forward) * caster.step_size
                    # y -= caster.step_size
                elif event.key == pygame.K_s or event.key == pygame.K_LEFT:
                    x -= math.cos(forward) * caster.step_size
                    y -= math.sin(forward) * caster.step_size
                    # y += caster.step_size
                elif event.key == pygame.K_a or event.key == pygame.K_UP:
                    x -= math.cos(right) * caster.step_size
                    y -= math.sin(right) * caster.step_size
                    # x -= caster.step_size
                elif event.key == pygame.K_d or event.key == pygame.K_DOWN:
                    x += math.cos(right) * caster.step_size
                    y += math.sin(right) * caster.step_size
                    # x += caster.step_size
                elif event.key == pygame.K_q:
                    caster.player['angle'] -= caster.turn_size
                    pass
                elif event.key == pygame.K_e:
                    caster.player['angle'] += caster.turn_size
                    pass

                # Evalúa que no haya pared para poderse mover
                i = int(x / caster.block_size)
                j = int(y / caster.block_size)

                if caster.map[j][i] == ' ':
                    caster.player['x'] = x
                    caster.player['y'] = y
            screen.fill(Color('gray'))

            # Techo
            screen.fill(Color('khaki'), (int(caster.width / 2), 0, int(caster.width / 2), int(caster.height / 2)))
            # Piso
            screen.fill(Color('wheat'),
                        (int(caster.width / 2), int(caster.height / 2), int(caster.width / 2), int(caster.height / 2)))

            caster.render(Color('navy'), TEXTURES)

            # FPS → frames per second
            # (0, 0, 30, 30) → x, y, width, height
            screen.fill(Color('black'), (0, 0, 34, 22))
            # Blit → dibujar objetos
            screen.blit(updateFps(), (0, 0))
            clock.tick(60)

    pygame.display.update()


