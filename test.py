import pygame

pygame.init()
pygame.display.set_mode((500, 500))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); #sys.exit() if sys is imported
        if event.type == pygame.KEYDOWN:
            print('Down ', event.key)
        if event.type == pygame.KEYUP:
            print('Up ', event.key)