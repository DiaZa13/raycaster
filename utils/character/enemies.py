import math

class Enemies(object):
    def __init__(self, x, y, texture):
        self.x = x
        self.y = y
        self.sprite = texture

    def draw(self, color, screen, size=5):
        rectangle = (self.x - size / 2, self.x - size / 2, size, size)
        screen.fill(color, rectangle)

    def addSprite(self, player, screen_height, screen_width,transform, size=30):
        # TODO optimizar calcular raiz cuadrada
        distance = ((player.x - self.x) ** 2 + (player.y - self.y) ** 2) ** 0.5
        # ángulo entre el enemigo y el jugador
        # TODO buscar formas de optimizar
        angle = math.atan2((self.y - player.y), (self.x - player.x))
        aspect_ratio = self.sprite.get_width() / self.sprite.get_height()
        height = (screen_height / distance) * size
        width = height * aspect_ratio

        # TODO a ti no te sirve Esto hay que modificarlo
        start_x = int((screen_width * 3 / 4) * (angle ) * screen_height / 2) - (width / 2)
        start_y = int(screen_height / 2) - (height / 2)

        texture = transform.scale(self.sprite, (width, height))
        pass
