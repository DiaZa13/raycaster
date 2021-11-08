import math
import sys
import os
from raycasterb import Raycaster
from pygame import font, Color, Surface, SRCALPHA
from utils.UI.text import Text
from character.player import Player
from map import Map


class GameWindow(object):
    def __init__(self, screen, draw, transform, clock, image, enemies):
        self.caster = Raycaster(screen, draw, transform, Player())
        self.caster.enemies = enemies
        self.clock = clock
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        self.transform = transform
        self.image = image
        self.pause = False
        self.resume = None
        self.start = None
        self.exit = None
        self.re_render = False
        self.level = 0
        self.levels = [True, False, False]

    def update_fps(self, color):
        fps = str(int(self.clock.get_fps()))
        fnt = font.Font('utils/fonts/RoseRegular.ttf', 30)
        fps = fnt.render(' ' + fps, False, color)
        return fps

    def move_options(self, event, pygame):
        playing = True
        x, y = 0, 0
        if event.type == pygame.KEYDOWN:
            if not self.pause:
                x = self.caster.player.x
                y = self.caster.player.y
                forward = self.caster.player.angle * math.pi / 180
                right = (self.caster.player.angle + 90) * math.pi / 180
                # Revisar que el evento se activo por la llave
                if event.key == pygame.K_ESCAPE:
                    self.re_render = True
                    self.pause = True
                    if self.pause:
                        self.pause_menu()
                        self.options()
                elif event.key == pygame.K_w or event.key == pygame.K_RIGHT:
                    # Para poder moverme con respecto al ángulo del jugador
                    x += math.cos(forward) * self.caster.player.step_size
                    y += math.sin(forward) * self.caster.player.step_size
                    # y -= self.caster.step_size
                elif event.key == pygame.K_s or event.key == pygame.K_LEFT:
                    x -= math.cos(forward) * self.caster.player.step_size
                    y -= math.sin(forward) * self.caster.player.step_size
                    # y += self.caster.player.step_size
                elif event.key == pygame.K_a or event.key == pygame.K_UP:
                    x -= math.cos(right) * self.caster.player.step_size
                    y -= math.sin(right) * self.caster.player.step_size
                    # x -= self.caster.player.step_size
                elif event.key == pygame.K_d or event.key == pygame.K_DOWN:
                    x += math.cos(right) * self.caster.player.step_size
                    y += math.sin(right) * self.caster.player.step_size
                    # x += self.caster.player.step_size
                elif event.key == pygame.K_q:
                    self.caster.player.angle -= self.caster.player.turn_size
                elif event.key == pygame.K_e:
                    self.caster.player.angle += self.caster.player.turn_size

                # Evalúa que no haya pared para poderse mover
                i = int(x / self.caster.map_surface.block_size)
                j = int(y / self.caster.map_surface.block_size)

                if self.caster.map_surface.map[j][i] == ' ':
                    self.caster.player.x = x
                    self.caster.player.y = y

                if 180 <= x <= 185 and 165 <= y <= 190 and self.levels[0]:
                    self.levels[1] = True
                    self.levels[0] = False
                    self.level = 1
                elif x == 180 and y == 65 and self.levels[1]:
                    self.levels[2] = True
                    self.levels[1] = False
                    self.level = 2

            else:
                if event.key == pygame.K_UP:
                    self.resume._hover = True
                    self.start._hover = False
                    self.exit._hover = False
                elif event.key == pygame.K_DOWN:
                    if self.resume._hover:
                        self.resume._hover = False
                        self.start._hover = True
                        self.exit._hover = False
                    elif self.start._hover:
                        self.resume._hover = False
                        self.start._hover = False
                        self.exit._hover = True
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    if self.resume._hover:
                        self.pause = False
                    if self.start._hover:
                        playing = False
                    elif self.exit._hover:
                        sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            if self.pause:
                if self.resume.rect.collidepoint(event.pos):
                    self.resume._hover = True
                    self.start._hover = False
                    self.exit._hover = False
                if self.start.rect.collidepoint(event.pos):
                    self.start._hover = True
                    self.resume._hover = False
                    self.exit._hover = False
                if self.exit.rect.collidepoint(event.pos):
                    self.exit._hover = True
                    self.resume._hover = False
                    self.start._hover = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.pause:
                if self.resume.rect.collidepoint(event.pos):
                    self.pause = False
                if self.start.rect.collidepoint(event.pos):
                    self.pause = False
                    playing = False
                if self.exit.rect.collidepoint(event.pos):
                    sys.exit()

        if self.pause:
            self.pause_menu()
            self.resume.draw_text()
            self.start.draw_text()
            self.exit.draw_text()

        return playing, x, y

    def floor_roof(self, fill_color, floor_color, roof_color):
        self.screen.fill(fill_color)
        # Techo
        self.screen.fill(roof_color,
                         (0, 0, int(self.width), int(self.height / 2)))
        # Piso
        self.screen.fill(floor_color,
                         (0, int(self.height / 2), int(self.width),
                          int(self.height / 2)))

    def render(self, color, e_color, textures, filename):
        self.caster.render(color, e_color, textures,  Map(filename, 500, 500))

    def clock_update(self, fps, bck_color, font_color):
        # FPS → frames per second
        # (0, 0, 30, 30) → x, y, width, height
        self.screen.fill(bck_color, (0, 0, 34, 22))
        # Blit → dibujar objetos
        self.screen.blit(self.update_fps(font_color), (0, 0))
        self.clock.tick(fps)

    def pause_menu(self):
        menu_bck = Surface((self.caster.width, self.caster.height), SRCALPHA)
        menu_bck.fill((7, 7, 7, 205))
        self.screen.blit(menu_bck, (0, 0))
        # Logo
        logo = self.image.load(os.path.join('utils/textures', 'logo2.png'))
        logo = self.transform.scale(logo, (180, 150))
        self.screen.blit(logo, [self.width / 2 - 90, 15])
        fnt = font.Font('utils/fonts/Pixel.ttf', 60)
        maze_pos = (self.width / 2, self.height / 2 - 20)
        maze = Text(self.screen, fnt, 'GAME PAUSED', maze_pos, Color('white'), center=True)

    def options(self):
        # Opciones
        fnt = font.Font('utils/fonts/Pixel.ttf', 40)
        resume_pos = (self.width / 2, int(1 / 2 * self.height + 60))
        self.resume = Text(self.screen, fnt, 'CONTINUE', resume_pos, Color('white'), Color('chartreuse'), fnt, True)
        self.resume._hover = True
        start_pos = (self.width / 2, int(1 / 2 * self.height) + 120)
        self.start = Text(self.screen, fnt, 'MAIN MENU', start_pos, Color('white'), Color('chartreuse'), fnt, True)
        exit_pos = (self.width / 2, int(1 / 2 * self.height) + 190)
        self.exit = Text(self.screen, fnt, 'QUIT GAME', exit_pos, Color('white'), Color('chartreuse'), fnt, True)

