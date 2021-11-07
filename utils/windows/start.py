from utils.UI.text import Text
import os
import sys
from pygame import font, Color, Surface, SRCALPHA


class StartWindow(object):
    def __init__(self, screen, image, transform, width, height):
        self.screen = screen
        self.image = image
        self.transform = transform
        self.width = width
        self.height = height
        self.x = None
        self.start = None
        self.exit = None

        self.background()
        self.tittle()
        self.option_menu()
        self.logo()
        self.options()

    def background(self):
        bck = self.image.load(os.path.join('utils/textures', 'night.png'))
        bck = self.transform.scale(bck, (self.width, self.height))
        self.screen.blit(bck, [0, 0])

    def tittle(self):
        fnt = font.Font('utils/fonts/Pixel.ttf', 120)
        maze_pos = (20, 2 / 4 * self.height)
        maze = Text(self.screen, fnt, 'MAZE', maze_pos, Color('white'))
        camping_pos = (20, self.height - 25 - maze.rect[3])
        Text(self.screen, fnt, 'CAMPING', camping_pos, Color('white'))

    def option_menu(self):
        # Menu de opciones
        self.x = self.width - int(1 / 4 * self.width) - 130
        menu_bck = Surface((int(1 / 3 * self.width), int(6 / 7 * self.height)), SRCALPHA)
        menu_bck.fill((229, 236, 231, 102))
        self.screen.blit(menu_bck, (self.x, 0))

    def logo(self):
        # Logo
        logo = self.image.load(os.path.join('utils/textures', 'logo2.png'))
        logo = self.transform.scale(logo, (180, 150))
        self.screen.blit(logo, [self.x + 80, 15])

    def options(self):
        # Opciones
        fnt = font.Font('utils/fonts/Pixel.ttf', 70)
        hover_font = font.Font('utils/fonts/Pixel.ttf', 70)
        start_pos = (self.x + 90, int(1 / 2 * self.height) - 40)
        self.start = Text(self.screen, fnt, 'PLAY', start_pos, Color('black'), Color('chartreuse'), hover_font)
        self.start._hover = True
        exit_pos = (self.x + 90, int(1 / 2 * self.height) + 60)
        self.exit = Text(self.screen, fnt, 'EXIT', exit_pos, Color('black'), Color('chartreuse'), hover_font)

    def move_options(self, event, pygame):
        playing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.start._hover = True
                self.exit._hover = False
            elif event.key == pygame.K_DOWN:
                self.start._hover = False
                self.exit._hover = True
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                if self.start._hover:
                    playing = True
                elif self.exit._hover:
                    sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            if self.start.rect.collidepoint(event.pos):
                self.start._hover = True
                self.exit._hover = False
            if self.exit.rect.collidepoint(event.pos):
                self.start._hover = False
                self.exit._hover = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.start.rect.collidepoint(event.pos):
                playing = True
            if self.exit.rect.collidepoint(event.pos):
                sys.exit()

        self.start.draw_text()
        self.exit.draw_text()

        return playing
