class Player(object):
    def __init__(self, x=100, y=100, fov=60, angle=0):
        self.x = x
        self.y = y
        self.fov = fov
        self.angle = angle
        # Pixeles que me muevo cada que presiono una tecla
        self.step_size = 5
        # Tamaño de los giros
        self.turn_size = 5

    def draw(self, color, screen, size=10):
        rectangle = (self.x - size / 2, self.y - size / 2, size, size)
        screen.fill(color, rectangle)
        # self.draw.circle(self.screen, color, (self.player['x'] - size / 2, self.player['y'] - size / 2), 5)

