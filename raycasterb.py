import math
from utils.character.enemies import Enemies

RAYS = 100


class Raycaster(object):
    def __init__(self, screen, draw, transform, enemies = None):
        self.screen = screen
        self.draw = draw
        self.transform = transform
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
        self.enemies = enemies

    def loadMap(self, filename):
        with open(filename) as file:
            for line in file.readlines():
                self.map.append(list(line))

    def drawBlock(self, x, y, texture):
        texture = self.transform.scale(texture, (self.block_size, self.block_size))
        rectangle = texture.get_rect().move(x, y)
        self.screen.blit(texture, rectangle)

    def drawPlayer(self, color, size=5):
        rectangle = (self.player['x'] - size / 2, self.player['y'] - size / 2, size, size)
        self.screen.fill(color, rectangle)
        # self.draw.circle(self.screen, color, (self.player['x'] - size / 2, self.player['y'] - size / 2), 5)

    # TODO mejorar implementación para ganar fps
    def ray(self, angle, color):
        ray_angle = angle * math.pi / 180
        # Revisando distancia por distancia por simplicidad
        distance = 0
        size_offset = 1
        x_offset = size_offset * math.cos(ray_angle)
        y_offset = size_offset * math.sin(ray_angle)
        x = self.player['x']
        y = self.player['y']
        while 1:
            distance += size_offset
            x += x_offset
            y += y_offset

            i = int(x / self.block_size)
            j = int(y / self.block_size)

            if j < len(self.map):
                if i < len(self.map[j]):
                    if self.map[j][i] != ' ':

                        hit_x = x - i * self.block_size
                        hit_y = y - j * self.block_size

                        hit = 0

                        if 1 < hit_x < self.block_size - 1:
                            if hit_y < 1:
                                hit = self.block_size - hit_x
                            elif hit_y >= self.block_size - 1:
                                hit = hit_x
                        elif 1 < hit_y < self.block_size - 1:
                            if hit_x < 1:
                                hit = hit_y
                            elif hit_x >= self.block_size - 1:
                                hit = self.block_size - hit_y

                        x_texture = hit / self.block_size

                        self.draw.line(self.screen, color, (self.player['x'], self.player['y']), (x, y))

                        return distance, self.map[j][i], x_texture

    def castRay(self, textures, ray_color, start_x, start_y):
        for column in range(RAYS):
            angle = (self.player['fov'] * column / RAYS) + self.player['angle'] - (self.player['fov'] / 2)
            distance, identifier, x_texture = self.ray(angle, ray_color)

            ray_width = int((1 / RAYS) * start_x) + 1
            x = start_x + int((column / RAYS) * start_x)
            # perceivedHeight = screenHeight / (distance * cos(rayAngle - viewAngle)) * wallHeight
            perceived_height = self.height / (
                    distance * math.cos((angle - self.player['angle']) * math.pi / 180)) * self.wall_height
            y = int(start_y - perceived_height / 2)

            # intensity = 1 - min(1, distance / self.max_distance)
            # color = (colors[int(identifier) - 1][0] * intensity,
            #          colors[int(identifier) - 1][1] * intensity,
            #          colors[int(identifier) - 1][2] * intensity)

            # TODO mejorar implementación así como la intensidad de la textura
            texture = textures[int(identifier) - 1]
            texture = self.transform.scale(texture, (texture.get_width() * ray_width, int(perceived_height)))
            x_texture = int(x_texture * texture.get_width())
            rectangle = (x_texture, 0, ray_width, texture.get_height())
            position = (x, int(y))
            self.screen.blit(texture, position, rectangle)

    def render(self, p_color, textures):
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
                    texture = textures[int(self.map[j][i]) - 1]
                    self.drawBlock(x, y, texture)

        # Player
        self.drawPlayer(p_color)
        # for enemy in self.enemies:
        #     enemy.draw(p_color, self.screen)
        self.castRay(textures, p_color, half_width, half_height)
