class Player(object):
    def __init__(self, x=100, y=100, fov=60, angle=0):
        self.x = x
        self.y = y
        self.fov = fov
        self.angle = angle

    def draw(self, color, screen, size=5):
        rectangle = (self.x - size / 2, self.y - size / 2, size, size)
        screen.fill(color, rectangle)
