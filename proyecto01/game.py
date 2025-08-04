import pygame
from sys import exit
from components.Button import Buttons
from components.Player import Player

pygame.init()
tk = pygame.display.set_mode((1200, 920))
pygame.display.set_caption("Flood")
clock = pygame.time.Clock()
escenarioActual = "arriba"


def game():
    mainPlayer = Player(tk)
    while(True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            mainPlayer.manejar_eventos(event)
        mainPlayer.movimiento()
        if mainPlayer.estado == "mesa":
            mainPlayer.dibujar_mesa()

        pygame.display.update()
        clock.tick(60)
        

def history():
    tk.fill("black")
    font = pygame.font.SysFont("Arial", 30)
    historia = ["Año 2130. La humanidad lucha por sobrevivir bajo tierra.",
                "Después de la gran inundación, todo cambió.",
                "Los bunkers se convirtieron en el único refugio seguro...",
                "Pero incluso ahí, no todos están a salvo."
            ]
    indexActual = 0
    alpha = 0 
    fading_in = True
    fading_out = False
    text_surface = font.render(historia[indexActual], True, (255,255,255))
    show_menu = True 
    fade_menu_alpha = 255
    menu_surface = pygame.Surface((800, 600))
    menu_surface.fill((0,0,0))
    menu_text = font.render("Presiona Enter para comenzar...", True, (255,255,255))
    menu_surface.blit(menu_text, (200,200))
    menu_surface.set_alpha(fade_menu_alpha)
    while True:
        tk.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if show_menu and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                show_menu = False
        if show_menu:
            tk.blit(menu_surface, (0,0))
        else:
            if fade_menu_alpha > 0:
                fade_menu_alpha -= 5
                menu_surface.set_alpha(fade_menu_alpha)
                tk.blit(menu_surface, (0,0))
            else:
                text_surface = font.render(historia[indexActual], True, (255,255,255))
                faded_text = text_surface.copy()
                faded_text.set_alpha(alpha)
                tk.blit(faded_text, (100, 280))
                if fading_in:
                    alpha += 3
                    if alpha >= 255:
                        alpha = 255
                        fading_in = False
                        pygame.time.set_timer(pygame.USEREVENT, 3000) #tiempo en ms
                elif fading_out:
                    alpha -= 3
                    if alpha <= 0:
                        alpha = 0 
                        fading_out = False
                        fading_in = True
                        indexActual += 1
                        if indexActual >= len(historia)-3:
                            game()
            if event.type == pygame.USEREVENT:
                fading_out = True
                pygame.time.set_timer(pygame.USEREVENT, 0)

        pygame.display.update()
        clock.tick(60)


def main_menu():
    icon = pygame.image.load(r"proyecto01\images\icon.png")
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()

    frameSurface = pygame.image.load(r"proyecto01\images\menu.jpeg") 
    frameSurface = pygame.transform.scale(frameSurface, (1200, 920))

    scaleStart = pygame.image.load(r"proyecto01\images\start.png")
    scaleStart = pygame.transform.scale(scaleStart, (350, 350))
    bgStart = scaleStart.get_at((0, 0))
    scaleStart.set_colorkey(bgStart)

    scaleHoverStart = pygame.image.load(r"proyecto01\images\start_hover.png")
    scaleHoverStart = pygame.transform.scale(scaleHoverStart, (350, 350))
    bgHoverStart = scaleHoverStart.get_at((0, 0))
    scaleHoverStart.set_colorkey(bgHoverStart)

    scaleQuit = pygame.image.load(r"proyecto01\images\quitScale.png")
    scaleQuit = pygame.transform.scale(scaleQuit, (250, 250))
    bgQuit = scaleQuit.get_at((0, 0))
    scaleQuit.set_colorkey(bgQuit)

    scaleQuitHover = pygame.image.load(r"proyecto01\images\quit_hover.png")
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
            history()
        pygame.display.update()
        clock.tick(60) #fps


if __name__ == "__main__":
    main_menu()

    