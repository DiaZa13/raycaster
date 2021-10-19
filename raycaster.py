import math
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [(255, 255, 255),
          (255, 0, 0),
          (0, 255, 0)]

WALLTEXTURES = {'1': 'test'}

RAYS = 20


class Raycaster(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        self.map = []
        self.block_size = 50
        self.wall_height = 50
        self.player = {'x': 0,
                       'y': 0,
                       'fov': 60,  # ángulo de visión
                       'angle': 0  # Dirección a la que se está viendo
                       }
        # Pixeles que me muevo cada que presiono una tecla
        self.step_size = 5
        # Tamaño de los giros
        self.turn_size = 5

    def loadMap(self, filename):
        with open(filename) as file:
            for line in file.readlines():
                self.map.append(list(line))

    def drawBlock(self, x, y, color):
        texture = WALLTEXTURES[color]
        texture = pygame.transform.scale(texture, self.block_size, self.block_size)
        rectangle = texture.get_rect()
        self.screen.blit(texture, rectangle)

    def drawPlayer(self, color, size=5):
        rectangle = (self.player['x'] - size / 2, self.player['y'] - size / 2, size, size)
        self.screen.fill

    def ray(self, color):
        # El rayo se dibujará en el mismo ángulo del jugador
        x = 0
        y = 0
        ray_angle = self.player['angle'] * math.pi / 180

        if ray_angle == 0 or ray_angle == math.pi:
            return None

        yo = 0
        xo = 0
        distance = 0
        # Teste con un solo rayo
        for r in range(1):
            # Check horizontal lines
            inv_tan = - 1 / math.tan(ray_angle)
            # Check if the ray is looking up/down
            if ray_angle > math.pi:  # down
                y = (int(self.player['y'] / self.block_size) * self.block_size) - 0.0001
                yo -= self.block_size
                x = (self.player['y'] - y) * inv_tan + self.player['x']
                xo = yo * inv_tan
            elif ray_angle < math.pi:  # up
                y = ((self.player['y'] / self.block_size) * self.block_size) + self.block_size
                yo = self.block_size
                x = (self.player['y'] - y) * inv_tan + self.player['x']
                xo = yo * inv_tan
        while distance < 8:
            i = int(x / self.block_size)
            j = int(y / self.block_size)

            if self.map[j][i] != ' ':
                break

            x += xo
            y += yo
            distance += 1

        self.draw.line(self.screen, color, (self.player['x'], self.player['y']), (x, y))

    # Generador de rayos
    def castRay(self, angle):
        radians = angle * math.pi / 180
        # Revisando distancia por distancia por simplicidad
        distance = 0
        while 1:
            x = int(self.player['x'] + distance * math.cos(angle))
            y = int(self.player['x'] + distance * math.sin(angle))

            i = int(x / self.block_size)
            j = int(y / self.block_size)

            if self.map[j][i] != ' ':
                return distance, self.map[j][i]

            self.screen.set_at((x, y), WHITE)
            distance += 1

    def render(self):
        for x in range(0, self.width, self.block_size):
            for y in range(0, self.height, self.block_size):
                # Cambiar la implementación para que se auto-adapte al tamaño de la pantalla
                # TODO adaptar a cualquier tamaño de pantalla
                i = int(x / self.block_size)
                j = int(y / self.block_size)
                if self.map[j][i] != ' ':
                    # Esto funciona ya que después en lugar de colores se utilizarán
                    # Diferentes texturas que cada identificador de pared
                    color = COLORS[int(self.map[j][i])]
                    self.drawBlock(x, y, color)

        for column in range(RAYS):
            angle = (self.player['fov'] * column / RAYS) + self.player['angle'] - (self.player['fov'] / 2)
            distance, identifier = self.castRay(angle)

            # Dibujar el bloque con el que hace contacto
            # for x in range(int(self.width / 2), self.width):
            # Cantidad con la que se representa cada uno de los rayos
            ray_width = (column / RAYS) * self.width / 2
            x = self.width / 2 + (column / RAYS) * self.width / 2
            # perceivedHeight = screenHeight / (distance * cos(rayAngle - viewAngle)) * wallHeight
            self.screen.fill(COLORS[identifier], (x, self.width / 2, ray_width, 20))
            # rectangle = (x, y, ray_width)
            h = 0
            '''
            Texturizar las paredes
            Se necesita dividir la textura por segmentos
            '''
            texture = WALLTEXTURES[identifier]
            texture = pygame.transform.scale(texture, (texture.get_width(), int(h)))
            rectangle = texture.get_rect()
            rectangle = rectangle.move((x, y))
            x_texture = column / RAYS * texture.get_width()

            area = (x_texture, 0, ray_width, h)

            self.screen.blit(texture, rectangle, area)

# Los eventos ocurren cada vez que algo pase
isRunning = True

while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            # x = caster.player['x']
            # y = caster.player['y']
            # forward = caster.player['angle'] * pi / 180
            # right =  (caster.player['angle'] + 90)  * pi / 180
            # Revisar que el evento se activo por la llave
            if event.key == pygame.K_ESCAPE:
                isRunning = False
            elif event.key == pygame.K_w:
                # Para poder moverme con respecto al ángulo del jugador
                # x += math.cos(angle) * caster.step_size
                # y += math.sin(angle) * caster.step_size
                pass
            elif event.key == pygame.K_s:
                # x -= math.cos(angle) * caster.step_size
                # y -= math.sin(angle) * caster.step_size
                pass
            elif event.key == pygame.K_a:
                # x -= math.cos(right) * caster.step_size
                # y -= math.sin(right) * caster.step_size
                pass
            elif event.key == pygame.K_d:
                # x += math.cos(right) * caster.step_size
                # y += math.sin(right) * caster.step_size
                pass
            elif event.key == pygame.K_q:
                # caster.player['angle] -= caster.turn_size
                pass
            elif event.key == pygame.K_e:
                # caster.player['angle] += caster.turn_size
                pass

            # Evalúa que no haya pared para poderse mover
            # i = int(x / self.block_size)
            # j = int(y / self.block_size)

            # if caster.map[j][i] == ' ':
            # caster.player['x'] = x
            # caster.player['y'] = y
