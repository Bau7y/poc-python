import pygame
from sys import exit
from components import Button

pygame.init()
tk = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Flood")

def main_menu():
    icon = pygame.image.load("proyecto01\images\icon.png")
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()

    frameSurface = pygame.image.load("proyecto01\images\menuFrame.png") 
    frameSurface = pygame.transform.scale(frameSurface, (1200, 800))
    bg = frameSurface.get_at((0, 0))
    frameSurface.set_colorkey(bg)

    scaleStart = pygame.image.load("proyecto01\images\start.png")
    scaleStart = pygame.transform.scale(scaleStart, (350, 350))
    bgStart = scaleStart.get_at((0, 0))
    scaleStart.set_colorkey(bgStart)

    scaleQuit = pygame.image.load("proyecto01\images\quitScale.png")
    scaleQuit = pygame.transform.scale(scaleQuit, (250, 250))
    bgQuit = scaleQuit.get_at((0, 0))
    scaleQuit.set_colorkey(bgQuit)


    while True:
        mousePos = pygame.mouse.get_pos()
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        tk.blit(frameSurface, (55, 7))
        tk.blit(scaleStart, (428, 100))
        tk.blit(scaleQuit, (522, 300))

        pygame.display.update()
        clock.tick(60) #fps


if __name__ == "__main__":
    main_menu()

    