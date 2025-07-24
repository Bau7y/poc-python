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

    scaleQuit = pygame.image.load("proyecto01\images\quitScale.png")
    scaleQuit = pygame.transform.scale(scaleQuit, (250, 250))
    bgQuit = scaleQuit.get_at((0, 0))
    scaleQuit.set_colorkey(bgQuit)


    while True:
        mousePos = pygame.mouse.get_pos()
        
        #startButton = Buttons(image=scaleStart, pos=(428,100), text="", font=get_font(75), base_color="Blue", hover_color="White")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        tk.blit(frameSurface, (0, 0))
        tk.blit(scaleStart, (25, 100))
        tk.blit(scaleQuit, (110, 300))

        pygame.display.update()
        clock.tick(60) #fps


if __name__ == "__main__":
    main_menu()

    