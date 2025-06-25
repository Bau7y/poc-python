#clase del humano
import random
from Reglas import ReglaTurno

class Humano:
    listaCartas = ["A de Corazones","2 de Corazones", "3 de Corazones", "4 de Corazones", "5 de Corazones", "6 de Corazones", "7 de Corazones", "8 de Corazones", "9 de Corazones", "10 de Corazones", "J de Corazones", "Q de Corazones", "K de Corazones",
                   "A de Diamantes","2 de Diamantes", "3 de Diamantes", "4 de Diamantes", "5 de Diamantes", "6 de Diamantes", "7 de Diamantes", "8 de Diamantes", "9 de Diamantes", "10 de Diamantes", "J de Diamantes", "Q de Diamantes", "K de Diamantes",
                   "A de Tréboles","2 de Tréboles", "3 de Tréboles", "4 de Tréboles", "5 de Tréboles", "6 de Tréboles", "7 de Tréboles", "8 de Tréboles", "9 de Tréboles", "10 de Tréboles", "J de Tréboles", "Q de Tréboles", "K de Tréboles",
                   "A de Picas","2 de Picas", "3 de Picas", "4 de Picas", "5 de Picas", "6 de Picas", "7 de Picas", "8 de Picas", "9 de Picas", "10 de Picas", "J de Picas", "Q de Picas", "K de Picas"]
    listaValores = [[4,8,4], [4,1,10], [8,3,6], [9,3,7], [8,1,8], [4,7,8], [7,5,4], [4,8,5], [7,1,10], [1,8,8], [7,7,6], [5,1,10], [7,8,5],
                    [2,7,10], [5,8,6], [6,8,1], [1,7,10], [3,4,10], [8,7,1], [5,5,5], [3,10,4], [9,8,1], [9,7,1], [1,5,10], [1,4,10], [5,5,5],
                    [2,4,10], [7,7,6], [7,10,1], [10,1,4], [1,9,7], [10,4,2], [6,8,1], [1,10,4], [4,10,2], [3,8,5], [7,6,6], [10,2,7], [9,1,6],
                    [10,5,5], [9,6,2], [2,9,4], [3,7,6], [8,8,3], [5,5,8], [7,4,6], [8,2,7], [3,10,5], [2,10,4], [4,6,5], [4,6,7], [3,5,8]]
    def __init__(self):
        self.__cartas = {} #diccionario de cartas

    def darCartas(self):
        for i in range(5):
            carta = random.randint(0,51)
            self.__cartas[self.listaCartas[carta]] = self.listaValores[carta]
        return self.__cartas
    
    
    def borrarMazo(self, mazo):
        for key, val in mazo.items():
            if key in self.listaCartas:
                self.listaCartas.remove(key)
                return self.listaCartas
            if val in self.listaValores:
                self.listaValores.remove(val)
                return self.listaValores
            
            