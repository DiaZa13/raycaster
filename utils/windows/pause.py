''' PAUSE MENU '''
# x = width - int(1 / 4 * width) - 50
# menu_bck = pygame.Surface((int(1 / 4 * width), int(3 / 4 * height)), pygame.SRCALPHA)
# menu_bck.fill((229, 236, 231, 102))
# screen.blit(menu_bck, (x, 0))
# delta_time = clock.tick(fps)

# Menu de opciones
x = width - int(1 / 4 * width) - 130
menu_bck = pygame.Surface((int(1 / 3 * width), int(6 / 7 * height)), pygame.SRCALPHA)
menu_bck.fill((229, 236, 231, 102))
screen.blit(menu_bck, (x, 0))