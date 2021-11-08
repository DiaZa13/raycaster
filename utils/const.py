from pygame import image
from character.sprites import Sprites

L1_TEXTURES = [image.load('utils/textures/level2.png'),
               image.load('utils/textures/wall1.png'),
               image.load('utils/textures/wall2.png'),
               image.load('utils/textures/wall3.png'),
               image.load('utils/textures/wall4.png'),
               image.load('utils/textures/wall5.png'),
               image.load('utils/textures/wall6.png')]

L2_TEXTURES = [image.load('utils/textures/level3.png'),
               image.load('utils/textures/land2.png'),
               image.load('utils/textures/land5.png'),
               image.load('utils/textures/land7.png'),
               image.load('utils/textures/land8.png'),
               image.load('utils/textures/land9.png')]


L3_TEXTURES = [image.load('utils/textures/level3.png'),
               image.load('utils/textures/wall7.png'),
               image.load('utils/textures/wall9.png'),
               image.load('utils/textures/tools.png'),
               image.load('utils/textures/stall.png'),
               image.load('utils/textures/window2.png'),
               image.load('utils/textures/door2.png'),
               image.load('utils/textures/furnace.png'),
               image.load('utils/textures/tend1.png'),
               image.load('utils/textures/tend2.png')]

L1_ENEMIES = [Sprites(90, 80, image.load('utils/sprites/enemy.png')),
              Sprites(440, 75, image.load('utils/sprites/enemy3.png')),
              Sprites(110, 300, image.load('utils/sprites/enemy2.png')),
              Sprites(400, 420, image.load('utils/sprites/enemy4.png'))]

L2_ENEMIES = [Sprites(90, 80, image.load('utils/sprites/enemy1.png')),
              Sprites(420, 75, image.load('utils/sprites/enemy5.png')),
              Sprites(390, 230, image.load('utils/sprites/decor1.png')),
              Sprites(400, 430, image.load('utils/sprites/enemy6.png')),
              Sprites(70, 230, image.load('utils/sprites/decor3.png'))]

L3_ENEMIES = [Sprites(90, 270, image.load('utils/sprites/decor_7.png')),
              Sprites(420, 75, image.load('utils/sprites/decor_8.png')),
              Sprites(90, 430, image.load('utils/sprites/decor_7.png'))]