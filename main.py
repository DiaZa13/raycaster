import pygame
from pygame import Color, image
import sys
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

width = 1024
height = 500
# Inicializando pygame
pygame.init()
draw = pygame.draw
transform = pygame.transform
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL)
# Solo para dar más velocidad
screen.set_alpha(None)
# Window tittle
pygame.display.set_caption('Raycaster')

# Raycaster
caster = Raycaster(screen, draw, transform)
caster.loadMap('./utils/maps/maze.txt')

# Referencia al reloj de pygame
clock = pygame.time.Clock()
font = pygame.font.Font('utils/fonts/RoseRegular.ttf', 30)


def updateFps():
    fps = str(int(clock.get_fps()))
    fps = font.render(' ' + fps, False, Color('white'))
    return fps


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Cierra la ventana de pygame
            sys.exit()
        elif event.type == pygame.KEYDOWN:
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
