import math
import sys
from raycasterb import Raycaster

class GameWindow(object):
    def __init__(self, screen, draw, transform, filename, clock, font):
        self.caster = Raycaster(screen, draw, transform)
        self.caster.loadMap(filename)
        self.clock = clock
        self.font = font
        self.screen = screen

    def update_fps(self, color):
        fps = str(int(self.clock.get_fps()))
        fps = self.font.render(' ' + fps, False, color)
        return fps

    def move_options(self, event, pygame):
        if event.type == pygame.KEYDOWN:
            x = self.caster.player['x']
            y = self.caster.player['y']
            forward = self.caster.player['angle'] * math.pi / 180
            right = (self.caster.player['angle'] + 90) * math.pi / 180
            # Revisar que el evento se activo por la llave
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.key == pygame.K_w or event.key == pygame.K_RIGHT:
                # Para poder moverme con respecto al ángulo del jugador
                x += math.cos(forward) * self.caster.step_size
                y += math.sin(forward) * self.caster.step_size
                # y -= self.caster.step_size
            elif event.key == pygame.K_s or event.key == pygame.K_LEFT:
                x -= math.cos(forward) * self.caster.step_size
                y -= math.sin(forward) * self.caster.step_size
                # y += self.caster.step_size
            elif event.key == pygame.K_a or event.key == pygame.K_UP:
                x -= math.cos(right) * self.caster.step_size
                y -= math.sin(right) * self.caster.step_size
                # x -= self.caster.step_size
            elif event.key == pygame.K_d or event.key == pygame.K_DOWN:
                x += math.cos(right) * self.caster.step_size
                y += math.sin(right) * self.caster.step_size
                # x += self.caster.step_size
            elif event.key == pygame.K_q:
                self.caster.player['angle'] -= self.caster.turn_size
            elif event.key == pygame.K_e:
                self.caster.player['angle'] += self.caster.turn_size

            # Evalúa que no haya pared para poderse mover
            i = int(x / self.caster.block_size)
            j = int(y / self.caster.block_size)

            if self.caster.map[j][i] == ' ':
                self.caster.player['x'] = x
                self.caster.player['y'] = y

    def floor_roof(self, fill_color, floor_color, roof_color):
        self.screen.fill(fill_color)
        # Techo
        self.screen.fill(roof_color,
                         (int(self.caster.width / 2), 0, int(self.caster.width / 2), int(self.caster.height / 2)))
        # Piso
        self.screen.fill(floor_color,
                         (int(self.caster.width / 2), int(self.caster.height / 2), int(self.caster.width / 2),
                          int(self.caster.height / 2)))

    def render(self, color, textures):
        self.caster.render(color, textures)

    def clock_update(self, fps, bck_color, font_color):
        # FPS → frames per second
        # (0, 0, 30, 30) → x, y, width, height
        self.screen.fill(bck_color, (0, 0, 34, 22))
        # Blit → dibujar objetos
        self.screen.blit(self.update_fps(font_color), (0, 0))
        self.clock.tick(fps)
