import math
from utils.character.enemies import Enemies

RAYS = 100

class Raycaster(object):
    def __init__(self, screen, draw, transform, player, map_surface, enemies=None):
        self.screen = screen
        self.draw = draw
        self.transform = transform
        _, _, self.width, self.height = screen.get_rect()
        self.wall_height = 50
        self.max_distance = 200
        self.map_surface = map_surface
        self.player = player
        self.enemies = enemies

    # TODO mejorar implementación para ganar fps
    def ray(self, angle, color):
        ray_angle = angle * math.pi / 180
        # Revisando distancia por distancia por simplicidad
        distance = 0
        size_offset = 1
        x_offset = size_offset * math.cos(ray_angle)
        y_offset = size_offset * math.sin(ray_angle)
        x = self.player.x
        y = self.player.y
        while 1:
            distance += size_offset
            x += x_offset
            y += y_offset

            i = int(x / self.map_surface.block_size)
            j = int(y / self.map_surface.block_size)

            if j < len(self.map_surface.map):
                if i < len(self.map_surface.map[j]):
                    if self.map_surface.map[j][i] != ' ':

                        hit_x = x - i * self.map_surface.block_size
                        hit_y = y - j * self.map_surface.block_size

                        hit = 0

                        if 1 < hit_x < self.map_surface.block_size - 1:
                            if hit_y < 1:
                                hit = self.map_surface.block_size - hit_x
                            elif hit_y >= self.map_surface.block_size - 1:
                                hit = hit_x
                        elif 1 < hit_y < self.map_surface.block_size - 1:
                            if hit_x < 1:
                                hit = hit_y
                            elif hit_x >= self.map_surface.block_size - 1:
                                hit = self.map_surface.block_size - hit_y

                        x_texture = hit / self.map_surface.block_size

                        # self.draw.line(self.screen, color, (self.player.x, self.player.y), (x, y))

                        return distance, self.map_surface.map[j][i], x_texture

    def castRay(self, textures, ray_color, start_y):
        for column in range(RAYS):
            angle = (self.player.fov * column / RAYS) + self.player.angle - (self.player.fov / 2)
            distance, identifier, x_texture = self.ray(angle, ray_color)

            ray_width = int((1 / RAYS) * self.width) + 1
            x = int((column / RAYS) * self.width)
            # perceivedHeight = screenHeight / (distance * cos(rayAngle - viewAngle)) * wallHeight
            perceived_height = self.height / (
                    distance * math.cos((angle - self.player.angle) * math.pi / 180)) * self.wall_height
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
        self.castRay(textures, p_color, self.height / 2)
        self.map_surface.render(textures, 100, 100, self.player, p_color, self.screen, self.height)

        # for enemy in self.enemies:
        #     enemy.draw(p_color, self.screen)
