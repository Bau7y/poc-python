import pygame
from sys import exit
from components.Button import Buttons


def get_font(size):
    return pygame.font.Font("proyecto01\images\start.png", size)

pygame.init()
tk = pygame.display.set_mode((1200, 920))
pygame.display.set_caption("Flood")

def main_menu():
    icon = pygame.image.load("proyecto01\images\icon.png")
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()

    frameSurface = pygame.image.load("proyecto01\images\menuFrame2.png") 
    frameSurface = pygame.transform.scale(frameSurface, (1200, 920))

    scaleStart = pygame.image.load("proyecto01\images\start.png")
    scaleStart = pygame.transform.scale(scaleStart, (350, 350))
    bgStart = scaleStart.get_at((0, 0))
    scaleStart.set_colorkey(bgStart)

    scaleHoverStart = pygame.image.load("proyecto01\images\start_hover.png")
    scaleHoverStart = pygame.transform.scale(scaleHoverStart, (350, 350))
    bgHoverStart = scaleHoverStart.get_at((0, 0))
    scaleHoverStart.set_colorkey(bgHoverStart)

    scaleQuit = pygame.image.load("proyecto01\images\quitScale.png")
    scaleQuit = pygame.transform.scale(scaleQuit, (250, 250))
    bgQuit = scaleQuit.get_at((0, 0))
    scaleQuit.set_colorkey(bgQuit)

    startButton = Buttons(25, 100, scaleStart, scaleHoverStart, scale=1)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        tk.blit(frameSurface, (0, 0))
        startButton.draw(tk)
        tk.blit(scaleQuit, (110, 300))

        pygame.display.update()
        clock.tick(60) #fps


if __name__ == "__main__":
    main_menu()

    