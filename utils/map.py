from pygame import Surface, transform
import math


class Map(object):
    def __init__(self, filename, width, height):
        self.map = []
        self.block_size = 50
        self.width = width
        self.height = height
        self.map_surface = Surface((self.width, self.height))
        self.map_surface.fill((229, 236, 231, 102))
        self.loadMap(filename)

    def loadMap(self, filename):
        with open(filename) as file:
            for line in file.readlines():
                self.map.append(list(line))

    def drawBlock(self, x, y, texture):
        texture = transform.scale(texture, (self.block_size, self.block_size))
        rectangle = texture.get_rect().move(x, y)
        self.map_surface.blit(texture, rectangle)

    def ray(self, angle, color, player, draw):
        ray_angle = angle * math.pi / 180
        # Revisando distancia por distancia por simplicidad
        distance = 0
        size_offset = 1
        x_offset = size_offset * math.cos(ray_angle)
        y_offset = size_offset * math.sin(ray_angle)
        x = player.x
        y = player.y
        while 1:
            distance += size_offset
            x += x_offset
            y += y_offset

            i = int(x / self.block_size)
            j = int(y / self.block_size)

            if j < len(self.map):
                if i < len(self.map[j]):
                    if self.map[j][i] != ' ' and self.map[j][i] != '0':

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

                        draw.line(self.map_surface, color, (player.x, player.y), (x, y))

                        return distance, self.map[j][i], x_texture

    def render(self, textures, width, height, player, p_color, enemies, e_color, screen, y, draw):
        for x in range(0, self.width, self.block_size):
            for y in range(0, self.height, self.block_size):
                # Cambiar la implementación para que se auto-adapte al tamaño de la pantalla
                # TODO adaptar a cualquier tamaño de pantalla
                i = int(x / self.block_size)
                j = int(y / self.block_size)

                if j < len(self.map):
                    if i < len(self.map[j]):
                        if self.map[j][i] != ' ':
                            # Esto funciona ya que después en lugar de colores se utilizarán
                            # Diferentes texturas que cada identificador de pared
                            texture = textures[int(self.map[j][i])]
                            self.drawBlock(x, y, texture)

        player.draw(p_color, self.map_surface)
        for enemy in enemies:
            enemy.draw(e_color, self.map_surface, draw)

        surface = transform.scale(self.map_surface, (width, height))
        screen.blit(surface, (0, y - width / 2))
