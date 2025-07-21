import pygame

pygame.init()

tk = pygame.display.set_mode((700, 500))

running = True 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()