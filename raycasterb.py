import math

RAYS = 50


class Raycaster(object):
    def __init__(self, screen, draw):
        self.screen = screen
        self.draw = draw
        _, _, self.width, self.height = screen.get_rect()
        self.map = []
        self.block_size = 50
        self.wall_height = 50
        self.player = {'x': 100,
                       'y': 100,
                       'fov': 60,  # ángulo de visión
                       'angle': 0  # Dirección a la que se está viendo
                       }
        # Pixeles que me muevo cada que presiono una tecla
        self.step_size = 5
        # Tamaño de los giros
        self.turn_size = 5
        self.max_distance = 200

    def loadMap(self, filename):
        with open(filename) as file:
            for line in file.readlines():
                self.map.append(list(line))

    def drawBlock(self, x, y, color):
        #     texture = WALLTEXTURES[color]
        #     texture = pygame.transform.scale(texture, self.block_size, self.block_size)
        #     rectangle = texture.get_rect()
        #     self.screen.blit(texture, rectangle)
        self.screen.fill(color, (x, y, self.block_size, self.block_size))

    def drawPlayer(self, color, size=5):
        rectangle = (self.player['x'] - size / 2, self.player['y'] - size / 2, size, size)
        self.screen.fill(color, rectangle)
        # self.draw.circle(self.screen, color, (self.player['x'] - size / 2, self.player['y'] - size / 2), 5)

    # TODO mejorar implementación para mejorar fps
    def ray(self, angle, color):
        ray_angle = angle * math.pi / 180
        # Revisando distancia por distancia por simplicidad
        distance = 0
        while 1:
            x = int(self.player['x'] + distance * math.cos(ray_angle))
            y = int(self.player['y'] + distance * math.sin(ray_angle))

            i = int(x / self.block_size)
            j = int(y / self.block_size)

            if j < len(self.map):
                if i < len(self.map[j]):
                    if self.map[j][i] != ' ':
                        return distance, self.map[j][i]

            self.screen.set_at((x, y), color)
            distance += 1

    def castRay(self, colors, ray_color, start_x, start_y, end_x=None, end_y=None):
        for column in range(RAYS):
            angle = (self.player['fov'] * column / RAYS) + self.player['angle'] - (self.player['fov'] / 2)
            distance, identifier = self.ray(angle, ray_color)

            ray_width = int((1 / RAYS) * start_x)
            x = start_x + int((column / RAYS) * start_x)
            # perceivedHeight = screenHeight / (distance * cos(rayAngle - viewAngle)) * wallHeight
            perceived_height = self.height / (
                        distance * math.cos((angle - self.player['angle']) * math.pi / 180)) * self.wall_height
            y = int(start_y - perceived_height / 2)
            rectangle = (x, y, ray_width + 1, perceived_height)

            intensity = 1 - min(1, distance / self.max_distance)
            color = (colors[int(identifier) - 1][0] * intensity,
                     colors[int(identifier) - 1][1] * intensity,
                     colors[int(identifier) - 1][2] * intensity)

            self.screen.fill(color, rectangle)

    def render(self, colors, p_color):
        half_width = self.width // 2
        half_height = self.height // 2
        for x in range(0, half_width - self.block_size, self.block_size):
            for y in range(0, self.height, self.block_size):
                # Cambiar la implementación para que se auto-adapte al tamaño de la pantalla
                # TODO adaptar a cualquier tamaño de pantalla
                i = int(x / self.block_size)
                j = int(y / self.block_size)
                if self.map[j][i] != ' ':
                    # Esto funciona ya que después en lugar de colores se utilizarán
                    # Diferentes texturas que cada identificador de pared
                    color = colors[int(self.map[j][i]) - 1]
                    self.drawBlock(x, y, color)

        # Player
        self.drawPlayer(p_color)

        self.castRay(colors, p_color, half_width, half_height)
