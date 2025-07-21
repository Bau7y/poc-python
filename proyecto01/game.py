import pygame
from sys import exit

pygame.init()

tk = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Flood")
icon = pygame.image.load("proyecto01\images\icon.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    pygame.display.update()
    clock.tick(60) #fps
    