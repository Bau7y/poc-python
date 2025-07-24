import pygame
from sys import exit
from components.Button import Buttons

pygame.init()
tk = pygame.display.set_mode((1200, 920))
pygame.display.set_caption("Flood")

def game():
    tk.fill("black")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        pygame.display.update()


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

    scaleQuitHover = pygame.image.load("proyecto01\images\quit_hover.png")
    scaleQuitHover = pygame.transform.scale(scaleQuitHover, (250, 250))
    bgQuitHover = scaleQuitHover.get_at((0, 0))
    scaleQuitHover.set_colorkey(bgQuitHover)

    startButton = Buttons(25, 100, scaleStart, scaleHoverStart, scale=1)
    quitButton = Buttons(110, 500, scaleQuit, scaleQuitHover, scale=1)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        tk.blit(frameSurface, (0, 0))
        startButton.draw(tk)
        quitButton.draw(tk)
        if Buttons.clicked(quitButton, event):
            pygame.quit()
            exit()
        elif Buttons.clicked(startButton, event):
            game()
        pygame.display.update()
        clock.tick(60) #fps


if __name__ == "__main__":
    main_menu()

    