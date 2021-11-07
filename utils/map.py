from pygame import Surface, transform


class Map(object):
    def __init__(self, filename, width, height):
        self.map = []
        self.block_size = 50
        self.width = width
        self.height = height
        self.map_surface = None

        self.loadMap(filename)

    def loadMap(self, filename):
        with open(filename) as file:
            for line in file.readlines():
                self.map.append(list(line))

    def drawBlock(self, x, y, texture):
        texture = transform.scale(texture, (self.block_size, self.block_size))
        rectangle = texture.get_rect().move(x, y)
        self.map_surface.blit(texture, rectangle)

    def render(self, textures, width, height, player, p_color, screen, y):
        self.map_surface = Surface((self.width, self.height))
        self.map_surface.fill((229, 236, 231, 102))
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
                            texture = textures[int(self.map[j][i]) - 1]
                            self.drawBlock(x, y, texture)

        player.draw(p_color, self.map_surface)
        # TODO renderizar villanos
        surface = transform.scale(self.map_surface, (width, height))
        screen.blit(surface, (0, y - width / 2))
