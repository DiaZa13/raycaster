import math


class Sprites(object):
    def __init__(self, x, y, texture):
        self.x = x
        self.y = y
        self.sprite = texture

    def draw(self, color, screen, draw, size=12):
        rectangle = (self.x - size / 2, self.y - size / 2)
        # screen.fill(color, rectangle)
        draw.circle(screen, color, rectangle, size)

    def addSprite(self, player, screen_height, screen_width, buffer, screen, size=30):
        # TODO optimizar calcular raiz cuadrada
        distance = ((player.x - self.x) ** 2 + (player.y - self.y) ** 2) ** 0.5
        # ángulo entre el enemigo y el jugador
        # TODO buscar formas de optimizar
        angle = math.atan2((self.y - player.y), (self.x - player.x)) * 180 / math.pi

        aspect_ratio = self.sprite.get_width() / self.sprite.get_height()
        height = (screen_height / distance) * size
        width = height * aspect_ratio

        # Punto inicial para dibujar sprite
        angle_dif = (angle - player.angle) % 360
        angle_dif = (angle_dif - 360) if angle_dif > 180 else angle_dif
        start_x = angle_dif * screen_width / player.fov
        start_x += (screen_width / 2) - (width / 2)
        start_y = int((screen_height / 2))
        start_x = int(start_x)

        for x in range(start_x, start_x + int(width)):
            if (0 < x < screen_width) and buffer[x] >= distance:
                for y in range(start_y, start_y + int(height)):
                    tx = int((x - start_x) * self.sprite.get_width() / width)
                    ty = int((y - start_y) * self.sprite.get_height() / height)
                    color = self.sprite.get_at((tx, ty))
                    if color[3] > 128:
                        screen.set_at((x, y), color)
