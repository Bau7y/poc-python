import pygame
from collections import Counter

class Player:
    def __init__(self, screen):
        self.screen = screen
        self.velocidad = 8
        self.player_w = 300
        self.player_h = 300
        self.debug = True

        # Estado animación / dirección
        self.dire = "down"
        self.frame = 0
        self.contador = 0
        self.frame_rate = 4

        # Cargar sprites una sola vez
        self.direcciones = {
            "up":    [pygame.image.load(r"proyecto01\images\walkUP-1.png").convert_alpha(),
                      pygame.image.load(r"proyecto01\images\walkUP-2.png").convert_alpha(),
                      pygame.image.load(r"proyecto01\images\walkUP-3.png").convert_alpha(),
                      pygame.image.load(r"proyecto01\images\walkUP-4.png").convert_alpha()],
            "down":  [pygame.image.load(r"proyecto01\images\walkDown-1.png").convert_alpha(),
                      pygame.image.load(r"proyecto01\images\walkDown-2.png").convert_alpha(),
                      pygame.image.load(r"proyecto01\images\walkDown-3.png").convert_alpha(),
                      pygame.image.load(r"proyecto01\images\walkDown-4.png").convert_alpha()],
            "right": [pygame.image.load(r"proyecto01\images\walkDerecha-1.png").convert_alpha(),
                      pygame.image.load(r"proyecto01\images\walkDerecha-2.png").convert_alpha(),
                      pygame.image.load(r"proyecto01\images\walkDerecha-3.png").convert_alpha(),
                      pygame.image.load(r"proyecto01\images\walkDerecha-4.png").convert_alpha()],
            "left":  [pygame.image.load(r"proyecto01\images\walkIzquierda-1.png").convert_alpha(),
                      pygame.image.load(r"proyecto01\images\walkIzquierda-2.png").convert_alpha(),
                      pygame.image.load(r"proyecto01\images\walkIzquierda-3.png").convert_alpha(),
                      pygame.image.load(r"proyecto01\images\walkIzquierda-4.png").convert_alpha()]
        }

        # Posición inicial 
        self.player_x, self.player_y = 0, 0

        # Cooldown para el gate
        self.portal_cd = 0

        # Cargar escena 1era
        self.cargar_escena("arriba")
        self.player_x, self.player_y = self.width // 2, self.height // 2

        #inventario
        self.inventario = Counter({"venda": 1, "medkit": 1})


    def add_item(self, item, qty=1):
        self.inventario[item] += qty

    def has_item(self, item, qty=1):
        return self.inventario.get(item, 0) >= qty
    
    def remove_item(self, item, qty=1):
        if self.has_item(item, qty):
            self.inventario[item] -= qty
            if self.inventario[item] <= 0:
                del self.inventario[item]
            return True
        return False

    def get_player_rect(self):
        return pygame.Rect(int(self.player_x), int(self.player_y), self.player_w, self.player_h)

    def cargar_escena(self, nombre):
        self.escena = nombre

        if nombre == "arriba":
            self.image = pygame.image.load(r"proyecto01\images\escenarioArriba.png").convert()
        elif nombre == "abajo":
            self.image = pygame.image.load(r"proyecto01\images\escenarioAbajo.png").convert()
        else:
            raise ValueError("Escena no válida")

        self.width, self.height = self.image.get_size()

        #puerta
        puerta_ancho = 96
        muro_grosor  = 28
        cx = self.width // 2

        muro_izq = pygame.Rect(0, self.height - muro_grosor,
                               cx - puerta_ancho // 2, muro_grosor)
        muro_der = pygame.Rect(cx + puerta_ancho // 2, self.height - muro_grosor,
                               self.width - (cx + puerta_ancho // 2), muro_grosor)

        # Paredes perimetrales
        pared = 24
        pared_sup = pygame.Rect(0, 0, self.width, pared)
        pared_izq = pygame.Rect(0, 0, pared, self.height)
        pared_der = pygame.Rect(self.width - pared, 0, pared, self.height)

        self.obstaculos = [muro_izq, muro_der, pared_sup, pared_izq, pared_der]

        # Trigger de cambio
        self.trigger_bajar = pygame.Rect(
            cx - puerta_ancho // 2,
            self.height - muro_grosor - 8,
            puerta_ancho,
            muro_grosor + 16
        )

        if nombre == "abajo":
            self.trigger_subir = pygame.Rect(
                cx - puerta_ancho // 2, 0, puerta_ancho, pared + 16
            )
        else:
            self.trigger_subir = None

    def mover_con_colision(self, dx, dy):
        rect = self.get_player_rect()

        # X
        rect.x += dx
        for o in self.obstaculos:
            if rect.colliderect(o):
                if dx > 0: rect.right = o.left
                elif dx < 0: rect.left  = o.right

        # Y
        rect.y += dy
        for o in self.obstaculos:
            if rect.colliderect(o):
                if dy > 0: rect.bottom = o.top
                elif dy < 0: rect.top    = o.bottom

        self.player_x, self.player_y = rect.x, rect.y

    def movimiento(self):
        dx = dy = 0
        teclas = pygame.key.get_pressed()
        moving = False

        if teclas[pygame.K_a]:
            dx -= self.velocidad; self.dire = "left";  moving = True
        elif teclas[pygame.K_d]:
            dx += self.velocidad; self.dire = "right"; moving = True
        elif teclas[pygame.K_w]:
            dy -= self.velocidad; self.dire = "up";    moving = True
        elif teclas[pygame.K_s]:
            dy += self.velocidad; self.dire = "down";  moving = True

        self.mover_con_colision(dx, dy)

        # cooldown
        if self.portal_cd > 0:
            self.portal_cd -= 1

        player_rect = self.get_player_rect()

        # De arriba - abajo
        if self.portal_cd == 0 and self.escena == "arriba" and player_rect.colliderect(self.trigger_bajar):
            self.cargar_escena("abajo")
            cx = self.width // 2
            self.player_x = cx - self.player_w // 2 - 70
            self.player_y = self.height - self.player_h - 24
            self.portal_cd = 50  # ~ 10 frames

        # De abajo - arriba
        elif self.portal_cd == 0 and self.escena == "abajo" and self.trigger_bajar and player_rect.colliderect(self.trigger_bajar):
            self.cargar_escena("arriba")
            cx = self.width // 2
            self.player_x = cx - self.player_w // 2 - 70
            self.player_y = self.height - 24 - self.player_h - 4
            self.portal_cd = 50

        # Clamps
        self.player_x = max(0, min(self.width  - self.player_w,  self.player_x))
        self.player_y = max(0, min(self.height - self.player_h,  self.player_y))

        #scrolls
        self.scroll_x = self.player_x - self.screen.get_width()  // 2
        self.scroll_y = self.player_y - self.screen.get_height() // 2
        self.scroll_x = max(0, min(self.width  - self.screen.get_width(),  self.scroll_x))
        self.scroll_y = max(0, min(self.height - self.screen.get_height(), self.scroll_y))

        #blits o draws
        self.screen.blit(self.image, (-self.scroll_x, -self.scroll_y))

        if self.debug:
            def draw_rect(r, color=(255, 0, 0, 120)):
                s = pygame.Surface((r.w, r.h), pygame.SRCALPHA); s.fill(color)
                self.screen.blit(s, (r.x - self.scroll_x, r.y - self.scroll_y))
            for o in self.obstaculos: draw_rect(o)
            draw_rect(self.trigger_bajar, (0,255,0,120))
            if self.trigger_subir: draw_rect(self.trigger_subir, (0,0,255,120))

        # Cambio de img (animaciones)
        if moving:
            self.contador += 1
            if self.contador >= self.frame_rate:
                self.contador = 0
                self.frame = (self.frame + 1) % len(self.direcciones[self.dire])
        else:
            self.dire = "down"
            self.frame = 0


        self.screen.blit(self.direcciones[self.dire][self.frame],
                         (self.player_x - self.scroll_x, self.player_y - self.scroll_y))
