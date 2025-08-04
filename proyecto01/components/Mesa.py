import pygame

class MesaInteractuable:
    def __init__(self, rect, objetos):
        nombres = [objeto.nombre for objeto in objetos]
        assert len(nombres) == len(set(nombres)), "Duplicado!"
        self.rect = rect
        self.objetos = objetos
        self.visible = True
        self.enabled = True


    def try_interactTable(self, player):
        if self.enabled:
            player.estado = "mesa"
            player.mesa_abierta = self


class ObjetoInteractivo:
    def __init__(self, imagen, nombre, valor, pos_ui):
        self.imagen = imagen
        self.nombre = nombre
        self.valor = valor
        self.rect = self.imagen.get_rect(topleft=pos_ui)