import math

RAYS = 100


class Raycaster(object):
    def __init__(self, screen, draw, transform, player):
        self.screen = screen
        self.draw = draw
        self.transform = transform
        _, _, self.width, self.height = screen.get_rect()
        self.wall_height = 40
        self.max_distance = 200
        self.map_surface = None
        self.player = player
        self.enemies = []
        self.zbuffer = [float('inf') for z in range(self.width)]

    def castRay(self, textures, ray_color, start_y):
        for column in range(RAYS):
            angle = (self.player.fov * column / RAYS) + self.player.angle - (self.player.fov / 2)
            distance, identifier, x_texture = self.map_surface.ray(angle, ray_color, self.player, self.draw)

            ray_width = int((1 / RAYS) * self.width) + 1

            # Z-buffer
            for i in range(ray_width - 1):
                self.zbuffer[column * (ray_width - 1) + i] = distance

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
            texture = textures[int(identifier)]
            texture = self.transform.scale(texture, (texture.get_width() * ray_width, int(perceived_height)))
            x_texture = int(x_texture * texture.get_width())
            rectangle = (x_texture, 0, ray_width, texture.get_height())
            position = (x, int(y))
            self.screen.blit(texture, position, rectangle)

    def render(self, p_color, e_color, textures, map_surface):
        self.map_surface = map_surface
        self.castRay(textures, p_color, self.height / 2)
        for enemy in self.enemies:
            enemy.addSprite(self.player, self.height, self.width, self.zbuffer, self.screen)

        self.map_surface.render(textures, 100, 100, self.player, p_color, self.enemies, e_color, self.screen,
                                self.height, self.draw)
