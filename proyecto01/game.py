import pygame
from sys import exit


pygame.init()

tk = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Flood")
icon = pygame.image.load("proyecto01\images\icon.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

frameSurface = pygame.image.load("proyecto01\images\menuFrame2.png") 
frameSurface = pygame.transform.scale(frameSurface, (1200, 800))
bg = frameSurface.get_at((0, 0))
frameSurface.set_colorkey(bg)

scaleStart = pygame.image.load("proyecto01\images\start.png")
scaleStart = pygame.transform.scale(scaleStart, (350, 350))
bgStart = scaleStart.get_at((0, 0))
scaleStart.set_colorkey(bgStart)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    tk.blit(frameSurface, (55, 7))
    tk.blit(scaleStart, (428, 100))

    pygame.display.update()
    clock.tick(60) #fps
    