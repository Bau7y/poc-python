import pygame

class Player:
    def __init__(self, image, screen, player):
        self.width, self.height = image.get_size()
        self.screen = screen
        self.player_x, self.player_y = self.width // 2, self.height // 2
        self.velocidad = 5
        self.player = player
        self.image = image

    def movimiento(self):
        self.direcciones = {"up": [], "down": [], "right": [], "left": []}
        dire = "down"
        self.frame = 0
        self.frame_rate = 10
        teclas = pygame.key.get_pressed()
        moving = False
        if teclas[pygame.K_a]:
            self.player_x -= self.velocidad
            dire = "left"
            moving = True
        elif teclas[pygame.K_d]:
            self.player_x += self.velocidad
            dire = "right"
            moving = True
        elif teclas[pygame.K_w]:
            self.player_y -= self.velocidad
            dire = "up"
            moving = True
        elif teclas[pygame.K_s]:
            self.player_y += self.velocidad
            dire = "down"
            moving = True

        self.player_x = max(0, min(self.width, self.player_x))
        self.player_y = max(0, min(self.height, self.player_y))

        self.scroll_x = self.player_x - self.screen.get_width() // 2
        self.scroll_y = self.player_y - self.screen.get_height() // 2

        self.scroll_x = max(0, min(self.width - self.screen.get_width(), self.scroll_x))
        self.scroll_y = max(0, min(self.height - self.screen.get_height(), self.scroll_y))

        self.screen.blit(self.image, (-self.scroll_x, -self.scroll_y))
        self.screen.blit(self.player, (self.player_x - self.scroll_x, self.player_y - self.scroll_y))

        self.contrador = 0
        if moving:
            self.contrador += 1
            if self.contrador >= self.frame_rate:
                self.contrador = 0
                self.frame = (self.frame + 1) % len(self.direcciones[dire])
        else:
            self.frame = 0
        self.screen.blit(self.direcciones[dire][self.frame], (self.player_x - self.scroll_x, self.player_y - self.scroll_y))

        