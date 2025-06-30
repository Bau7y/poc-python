#Clase de la IA 
import random
from Reglas import ReglaTurno

class Bot:
    listaCartas = [["A de Corazones","2 de Corazones", "3 de Corazones", "4 de Corazones", "5 de Corazones", "6 de Corazones", "7 de Corazones", "8 de Corazones", "9 de Corazones", "10 de Corazones", "J de Corazones", "Q de Corazones", "K de Corazones",
                   "A de Diamantes","2 de Diamantes", "3 de Diamantes", "4 de Diamantes", "5 de Diamantes", "6 de Diamantes", "7 de Diamantes", "8 de Diamantes", "9 de Diamantes", "10 de Diamantes", "J de Diamantes", "Q de Diamantes", "K de Diamantes",
                   "A de Tréboles","2 de Tréboles", "3 de Tréboles", "4 de Tréboles", "5 de Tréboles", "6 de Tréboles", "7 de Tréboles", "8 de Tréboles", "9 de Tréboles", "10 de Tréboles", "J de Tréboles", "Q de Tréboles", "K de Tréboles",
                   "A de Picas","2 de Picas", "3 de Picas", "4 de Picas", "5 de Picas", "6 de Picas", "7 de Picas", "8 de Picas", "9 de Picas", "10 de Picas", "J de Picas", "Q de Picas", "K de Picas"],
                   [[5,1,9],[10,1,9],[9,3,4],[7,6,2],[4,10,4],[8,5,3],[5,9,2],[8,7,1],[4,7,8],[7,3,10],[3,8,7],[5,4,6],[10,5,5],
                   [8,4,4],[3,7,10],[2,6,9],[2,9,5],[10,6,1],[2,8,8],[7,1,7],[1,7,10],[5,1,10],[9,4,3],[10,3,5],[6,8,3],[8,2,9],
                   [2,9,4],[3,8,4],[2,8,9],[4,10,1],[4,9,2],[9,1,9],[2,9,6],[7,8,3],[3,8,4],[6,6,3],[8,6,1],[8,5,5],[10,1,5],
                   [3,6,7],[6,1,10],[3,7,5],[2,4,10],[7,6,6],[7,4,6],[4,6,7],[1,5,10],[8,6,4],[2,7,8],[8,6,6],[3,10,5],[3,6,7]]]
    

    def __init__(self):
        self.__baraja = {} #diccionario de cartas


    def darCartas(self):
        for i in range(5):
            carta = random.randint(0,len(self.listaCartas[0])-1)
            self.__baraja[self.listaCartas[0][carta]] = self.listaCartas[1][carta]
        return self.__baraja
    
    
    def analisis(self, baraja, regla, rondas):
        self.cartaSeleccionada = {}
        if rondas["ganadas"] == 2:
            for key, val in baraja.items():
                if ReglaTurno(val[0], val[1], val[2]).SumaTodo() >= 15:
                    self.cartaSeleccionada[key] = val
                    return self.cartaSeleccionada
        if regla == 0:
            for key, val in baraja.items():
                if ReglaTurno(val[0], val[1], val[2]).SumaConocimientoEstrategia() >= 8:
                    self.cartaSeleccionada[key] = val
                    return self.cartaSeleccionada
        elif regla == 1:
            for key, val in baraja.items():
                if ReglaTurno(val[0],val[1],val[2]).SumaEstrategiaEnergia() >= 8:
                    self.cartaSeleccionada[key] = val
                    return self.cartaSeleccionada
        elif regla == 2:
            for key, val in baraja.items():
                if ReglaTurno(val[0], val[1], val[2]).ConocimientoMenosEnergia() >= 7:
                    self.cartaSeleccionada[key] = val
                    return self.cartaSeleccionada
        elif regla == 3:
            for key, val in baraja.items():
                if ReglaTurno(val[0], val[1], val[2]).SumaTodo() >= 12:
                    self.cartaSeleccionada[key] = val
                    return self.cartaSeleccionada
        elif regla == 4:
            for key, val in baraja.items():
                if ReglaTurno(val[0], val[1], val[2]).EstrategiaPorEnergia() >= 16:
                    self.cartaSeleccionada[key] = val
                    return self.cartaSeleccionada


    def borrarMazo(self, mazo):
        for key, val in mazo.items():
            if key in self.listaCartas[0]:
                self.listaCartas[0].remove(key)
                return self.listaCartas
            if val in self.listaCartas[1]:
                self.listaCartas[1].remove(val)
                return self.listaCartas