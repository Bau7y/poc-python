import pygame
from collections import Counter
from components.Interact import Interact
from components.Mesa import *

class Player:
    def __init__(self, screen):
        self.screen = screen
        self.velocidad = 8
        self.player_w = 75
        self.player_h = 125
        self.debug = False
        self.obj_tomado = False

        #tiempoLimite
        self.tiempoLimite = 300
        self.tiempoRestante = self.tiempoLimite
        self.tiempoUltimoTick = pygame.time.get_ticks()
        self.partidaTerminada = False

        # Estado animación / dirección
        self.dire = "down"
        self.frame = 0
        self.contador = 0
        self.frame_rate = 4
        self.stats = {"puntos": 0}

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

        #objetos
        objCO2 = pygame.image.load(r"proyecto01\images\bombonaOxigeno.png").convert_alpha()
        objCO2 = pygame.transform.scale(objCO2, (300, 300))
        bgCO2 = objCO2.get_at((0, 0))
        objCO2.set_colorkey(bgCO2)
        objVenda = pygame.image.load(r"proyecto01\images\venda.png").convert_alpha()
        objVenda = pygame.transform.scale(objVenda, (300, 300))
        bgVenda = objVenda.get_at((0, 0))
        objVenda.set_colorkey(bgVenda)
        objPill = pygame.image.load(r"proyecto01\images\pill.png").convert_alpha()
        objPill = pygame.transform.scale(objPill, (300, 300))
        bgPill = objPill.get_at((0, 0))
        objPill.set_colorkey(bgPill)
        objWater = pygame.image.load(r"proyecto01\images\botellaAgua.png").convert_alpha()
        objWater = pygame.transform.scale(objWater, (300, 300))
        bgWater = objWater.get_at((0, 0))
        objWater.set_colorkey(bgWater)
        objBotiquin = pygame.image.load(r"proyecto01\images\botiquin.png").convert_alpha()
        objBotiquin = pygame.transform.scale(objBotiquin, (300, 300))
        bgBotiquin = objBotiquin.get_at((0, 0))
        objBotiquin.set_colorkey(bgBotiquin)
        objCanasta = pygame.image.load(r"proyecto01\images\canasta.png").convert_alpha()
        objCanasta = pygame.transform.scale(objCanasta, (300, 300))
        bgCanasta = objCanasta.get_at((0, 0))
        objCanasta.set_colorkey(bgCanasta)
        #npcs
        npcImg1 = pygame.image.load(r"proyecto01\images\personajeNpc1.png").convert_alpha()
        npcImg2 = pygame.image.load(r"proyecto01\images\personajeNpc2.png").convert_alpha()
        npcImg3 = pygame.image.load(r"proyecto01\images\personajeNpc3.png").convert_alpha()

        self.mesa = MesaInteractuable(
            rect=pygame.Rect(100, 655, 200, 90),
            objetos=[
                ObjetoInteractivo(imagen=objCO2, nombre="CO2", valor=150, pos_ui=(100, 100)),
                ObjetoInteractivo(imagen=objVenda, nombre="venda", valor=60, pos_ui=(400, 100)),
                ObjetoInteractivo(imagen=objPill, nombre="pildora", valor=70, pos_ui=(700, 100)),
                ObjetoInteractivo(imagen=objWater, nombre="agua", valor=50, pos_ui=(100, 500)),
                ObjetoInteractivo(imagen=objBotiquin, nombre="medKit", valor=200, pos_ui=(400, 500)),
                ObjetoInteractivo(imagen=objCanasta, nombre="canasta", valor=500, pos_ui=(700, 500))
            ]
        )

        self.npcA = Interact(
                rect=pygame.Rect(300, 500, 20, 20),
                name="Paciente A",
                required_item="venda",
                img= npcImg1,
                thanks_msg="Gracias por la venda",
                request_msg="Necesito una venda"
            )
        self.npcB = Interact(
                rect=pygame.Rect(400, 900, 30, 40),
                name="Paciente B",
                required_item="CO2",
                img= npcImg2,
                thanks_msg="Gracias por la bombona de oxigeno",
                request_msg="Necesito una bombona de oxigeno"
            )
        self.npcC = Interact(
                rect=pygame.Rect(800, 650, 30, 40),
                name="Paciente C",
                required_item="canasta",
                img= npcImg3,
                thanks_msg="Gracias por la canasta",
                request_msg="Necesito una canasta de viveres"
            )
        self.npcs_escena = {"arriba": [self.npcA],
                            "abajo": [self.npcB, self.npcC]}

        # Cargar escena 1era
        self.cargar_escena("arriba")
        self.player_x, self.player_y = self.width // 2, self.height // 2

        #inventario
        self.inventario = Counter({})

        self.font = pygame.font.SysFont("Arial", 24)


    def add_item(self, item, valor):
        self.inventario[item] += valor

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
        self.interactables = []
        self.npcs = self.npcs_escena.get(nombre, [])
        self.estado = "jugando"
        self.escena = nombre
        
        if nombre == "arriba":
            self.image = pygame.image.load(r"proyecto01\images\escenarioArriba.png").convert()
            self.interactables.append(self.mesa)
            print("Npcs cargados: ", [npc.name for npc in self.npcs])
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
                               cx - puerta_ancho // 2 + 30, muro_grosor)
        muro_der = pygame.Rect(cx + puerta_ancho // 2 - 30, self.height - muro_grosor,
                               self.width - (cx + puerta_ancho // 2) + 30, muro_grosor)

        # Paredes perimetrales
        pared = 24
        pared_sup = pygame.Rect(0, 0, self.width, pared)
        pared_izq = pygame.Rect(0, 0, pared + 25, self.height)
        pared_der = pygame.Rect(self.width - pared - 30, 0, pared + 28, self.height)

        #hitboxes arriba
        camas_der_abajo = pygame.Rect(938, 750, 200, 400)
        camas_der_arriba = pygame.Rect(750, 300, 440, 270)
        camilla_arriba = pygame.Rect(530, 300, 210, 300)
        muro_puerta = pygame.Rect(0, 320, 600, 10)
        muroA_abajo_der = pygame.Rect(700, 1040, 499, 190)
        muroA_abajo_izq = pygame.Rect(0, 1040, 499, 189)

        #hitboxes abajo
        muroB_abajo_der = pygame.Rect(700, 1590, 499, 190)
        muroB_abajo_izq = pygame.Rect(0, 1590, 499, 189)
        camas_izq_abajo = pygame.Rect(130, 1180, 220, 280)
        camas_izq_arriba = pygame.Rect(100, 670, 250, 230)
        camas_der = pygame.Rect(810, 810, 260, 650)
        muro_pared = pygame.Rect(0, 450, self.width, pared)
        camilla_abajo = pygame.Rect(self.width // 2 - 100, 470, 200, 180)

        
        if self.escena == "arriba":
            self.obstaculos = [muro_izq, muro_der, pared_sup, pared_izq, pared_der, camas_der_abajo,
                                camas_der_arriba, muroA_abajo_der, muroA_abajo_izq, camilla_arriba, muro_puerta, self.mesa.rect]
            for npc in self.npcs:
                if npc.enabled:
                    self.obstaculos.append(npc.block_rect)
        else: 
            self.obstaculos = [muro_izq, muro_der, pared_sup, pared_izq, pared_der, camas_izq_abajo, muroB_abajo_der,
                                muroB_abajo_izq, muro_pared, camas_izq_arriba, camas_der, camilla_abajo]
            for npc in self.npcs:
                if npc.enabled:
                    self.obstaculos.append(npc.block_rect)

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


    def get_use_zone(self, player_rect, facing, area=40):
        if facing == "up":
            return pygame.Rect(player_rect.centerx - 12, player_rect.top - area, 24, area)
        if facing == "down":
            return pygame.Rect(player_rect.centerx - 12, player_rect.bottom, 24, area)
        if facing == "left":
            return pygame.Rect(player_rect.left - area, player_rect.centery, area, player_rect.height)
        if facing == "right":
            return pygame.Rect(player_rect.right, player_rect.centery - 12, area, 24)
        return player_rect.copy()
    
    def dibujar_mesa(self):
        # Fondo oscuro
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        # Título
        if not self.obj_tomado:
            titulo = self.font.render("Selecciona un objeto", True, (255, 255, 255))
            self.screen.blit(titulo, (self.screen.get_width() // 2 - titulo.get_width() // 2, 50))
        else:
            titulo = self.font.render("Ya seleccionaste un objeto", True, (255, 255, 255))
            self.screen.blit(titulo, (self.screen.get_width() // 2 - titulo.get_width() // 2, 50))

        # Dibujar objetos de la mesa
        mesa = self.mesa_abierta
        for obj in mesa.objetos:
            self.screen.blit(obj.imagen, obj.rect.topleft)
            nombre = self.font.render(f"{obj.nombre} - valor: {obj.valor}", True, (255, 255, 255))
            self.screen.blit(nombre, (obj.rect.left, obj.rect.bottom + 5))

    def game_over(self):
        self.estado = "gameover"
        self.screen.fill((0, 0, 0))
        game_over_text = self.font.render(f"¡Tiempo agotado! Fin del juego. \n Total Puntos {self.stats["puntos"]}", True, (255, 0, 0))
        self.screen.blit(game_over_text, (self.width // 2 - game_over_text.get_width() // 2, self.height // 2 - game_over_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        

    def movimiento(self):
        if not self.partidaTerminada:
            ahora = pygame.time.get_ticks()
            delta = (ahora - self.tiempoUltimoTick) / 1000
            self.tiempoUltimoTick = ahora

            self.tiempoRestante -= delta
            minutos = int(self.tiempoRestante // 60)
            segundos = int(self.tiempoRestante % 60)
            self.tiempoRestante_str = f"{minutos:02d}:{segundos:02d}"
            if self.tiempoRestante <= 0:
                self.partidaTerminada = True
                self.tiempoRestante = 0
                print("¡Tiempo agotado! Fin del juego.")
                self.estado = "gameover"

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
            self.player_x = cx - self.player_w // 2
            self.player_y = self.height - self.player_h + 40
            self.portal_cd = 100  # ~ 10 frames

        # De abajo - arriba
        elif self.portal_cd == 0 and self.escena == "abajo" and self.trigger_bajar and player_rect.colliderect(self.trigger_bajar):
            self.cargar_escena("arriba")
            cx = self.width // 2
            self.player_x = cx - self.player_w // 2
            self.player_y = self.height - 24 - self.player_h + 40
            self.portal_cd = 100

        # Clamps
        self.player_x = max(0, min(self.width  - self.player_w,  self.player_x))
        self.player_y = max(0, min(self.height - self.player_h,  self.player_y))

        #scrolls
        self.scroll_x = self.player_x - self.screen.get_width()  // 2
        self.scroll_y = self.player_y - self.screen.get_height() // 2
        self.scroll_x = max(0, min(self.width  - self.screen.get_width(),  self.scroll_x))
        self.scroll_y = max(0, min(self.height - self.screen.get_height(), self.scroll_y))

        #npc colision

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

        for npc in self.npcs: npc.draw(self.screen, self.scroll_x, self.scroll_y)

        self.screen.blit(self.direcciones[self.dire][self.frame],
                         (self.player_x - self.scroll_x, self.player_y - self.scroll_y))
        
        tiempo_txt = self.font.render(f"Tiempo restante: {self.tiempoRestante_str}", True, (255, 255, 255))
        self.screen.blit(tiempo_txt, (20, 20))

        puntos_txt = self.font.render(f"Puntos: {self.stats["puntos"]}", True, (255, 255, 255))
        self.screen.blit(puntos_txt, (20, 60))
        
        
    def manejar_eventos(self, event):
        if self.estado == "mesa":
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for obj in self.mesa_abierta.objetos:
                    if obj.rect.collidepoint(pos):
                        if not self.obj_tomado:
                            self.obj_tomado = True
                            self.add_item(obj.nombre, obj.valor)
                            self.mesa_abierta.objetos.remove(obj)
                            print(f"Objeto {obj.nombre} agregado al inventario.")
                            self.estado = "jugando"
                            self.mesa_abierta = None
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.estado = "jugando"
                self.mesa_abierta = None
        elif self.estado == "jugando":
            player_rect = self.get_player_rect()
            use_zone = self.get_use_zone(player_rect, self.dire, 40)

            candidato = None
            for npc in self.npcs:
                if npc.enabled and use_zone.colliderect(npc.rect):
                    candidato = npc
                    print("Candidato encontrado:", candidato.name)
                    break

            if candidato:
                prompt = self.font.render(f"Presiona E para interaccionar con {candidato.name}", True, (255, 255, 255))
                self.screen.blit(prompt, (candidato.rect.centerx - self.scroll_x - 6,
                                        candidato.rect.top - 18 - self.scroll_y))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e and candidato:
                texto = candidato.try_interact(self)
                if texto:
                    print("Texto:", texto)

            candidatoMesa = None
            for mesa in self.interactables:
                if mesa.enabled and use_zone.colliderect(mesa.rect):
                    candidatoMesa = mesa
                    break
            if candidatoMesa and event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                candidatoMesa.try_interactTable(self)
                        

