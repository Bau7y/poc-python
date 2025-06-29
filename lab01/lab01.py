import random, os
from HumanClass import *
from IaClass import *
from Reglas import ReglaTurno


def mostrarStats(punto, regla, dicRonda):
    os.system("cls")
    print("---------------Humano vs IA---------------\nRegla de la ronda: ", regla, "\n\n")
    if punto == 1:
        dicRonda["ganadas"] += 1
    elif punto == 2:
        dicRonda["perdidas"] += 1
    else:
        pass
    for llave, valor in dicRonda.items():
        print(llave, ": ", valor)
    os.system("pause")


def ganador(cartaHumano, cartaIa, regla):
    if regla == 0:
        #Conocimiento más estrategia
        for llaveHumano, valorHumano in cartaHumano.items():
            puntosH = ReglaTurno(valorHumano[0], valorHumano[1], valorHumano[2]).SumaConocimientoEstrategia()
        for llaveIa, valorIa in cartaIa.items():
            puntosIa = ReglaTurno(valorIa[0], valorIa[1], valorIa[2]).SumaConocimientoEstrategia()
        if puntosH > puntosIa:
            print("\nGanador: Humano\n", "carta: ", llaveHumano)
            return 1
        elif puntosH < puntosIa:
            print("\nGanador: Ia\n", "carta: ", llaveIa)
            return 2
        elif puntosH == puntosIa:
            print("\nEmpate\n")
            return 0
    elif regla == 1:
        #SumaEstrategiaEnergia
        for llaveHumano, valorHumano in cartaHumano.items():
            puntosH = ReglaTurno(valorHumano[0], valorHumano[1], valorHumano[2]).SumaEstrategiaEnergia()
        for llaveIa, valorIa in cartaIa.items():
            puntosIa = ReglaTurno(valorIa[0], valorIa[1], valorIa[2]).SumaEstrategiaEnergia()
        if puntosH > puntosIa:
            print("\nGanador: Humano\n", "carta: ", llaveHumano)
            return 1
        elif puntosH < puntosIa:
            print("\nGanador: Ia\n", "carta: ", llaveIa)
            return 2
        elif puntosH == puntosIa:
            print("\nEmpate\n")
    elif regla == 2:
        #ConocimientoMenosEnergia
        for llaveHumano, valorHumano in cartaHumano.items():
            puntosH = ReglaTurno(valorHumano[0], valorHumano[1], valorHumano[2]).ConocimientoMenosEnergia()
        for llaveIa, valorIa in cartaIa.items():
            puntosIa = ReglaTurno(valorIa[0], valorIa[1], valorIa[2]).ConocimientoMenosEnergia()
        if puntosH > puntosIa:
            print("\nGanador: Humano\n", "carta: ", llaveHumano)
            return 1
        elif puntosH < puntosIa:
            print("\nGanador: Ia\n", "carta: ", llaveIa)
            return 2
        elif puntosH == puntosIa:
            print("\nEmpate\n")
            return 0
    elif regla == 3:
        #SumaTodo
        for llaveHumano, valorHumano in cartaHumano.items():
            puntosH = ReglaTurno(valorHumano[0], valorHumano[1], valorHumano[2]).SumaTodo()
        for llaveIa, valorIa in cartaIa.items():
            puntosIa = ReglaTurno(valorIa[0], valorIa[1], valorIa[2]).SumaTodo()
        if puntosH > puntosIa:
            print("\nGanador: Humano\n", "carta: ", llaveHumano)
            return 1
        elif puntosH < puntosIa:
            print("\nGanador: Ia\n", "carta: ", llaveIa)
            return 2
        elif puntosH == puntosIa:
            print("\nEmpate\n")
            return 0
    elif regla == 4:
        #EstrategiaPorEnergia
        for llaveHumano, valorHumano in cartaHumano.items():
            puntosH = ReglaTurno(valorHumano[0], valorHumano[1], valorHumano[2]).EstrategiaPorEnergia()
        for llaveIa, valorIa in cartaIa.items():
            puntosIa = ReglaTurno(valorIa[0], valorIa[1], valorIa[2]).EstrategiaPorEnergia()
        if puntosH > puntosIa:
            print("\nGanador: Humano\n", "carta: ", llaveHumano)
            return 1
        elif puntosH < puntosIa:
            print("\nGanador: Ia\n", "carta: ", llaveIa)
            return 2
        elif puntosH == puntosIa:
            print("\nEmpate\n")
            return 0
    

def showIa(regla):
    print("---------------Humano vs IA---------------\nRegla de la ronda: ", regla, "\n\n")
    print("\n\nTurno de que la Ia elija su carta...\n")
    os.system("pause")


def solicitarCarta(mazo):
    while(True):
        try:
            option = input("\nSeleccione una carta(# de ????): ")
            for key, val in mazo.items():
                if option == key:
                    selectedCard = {key: val}
                    print("\nCarta seleccionada: ", selectedCard)
                    return selectedCard
            print("\nNo se ha encontrado la carta solicitada\n")
        except:
            print("Solo se admiten numeros...")


def mostrarCartas(mazo):
    carta=0
    while(carta < 5):
        for key, value in mazo.items():
            carta +=1
            print(f"{carta}. ",key, value)


def game():
    rondas = {"ganadas": 0, "perdidas": 0}
    while(True):
        listaReglas = ["conocimiento + estrategia", "estrategia + energía", "(conocimiento * 2) - energía", "conocimiento + estrategia + energía", "estrategia * energía"]
        index = random.randint(0,4)
        human = Humano()
        ia = Bot()
        mazoH = human.darCartas()
        os.system("cls")
        print("---------------Humano vs IA---------------\nRegla de la ronda: ", listaReglas[index], "\n\nGana quien obtenga el mayor puntaje acorde a la regla\n\n[conocimiento, estrategia y energía]\n[    #   ,   #   ,   #   ]\n\n")
        mostrarCartas(mazoH)
        carta = solicitarCarta(mazoH)
        os.system("pause")
        os.system("cls")
        showIa(listaReglas[index])
        mazoIa = ia.darCartas()
        cartaIa = ia.analisis(mazoIa, index, rondas)
        print(cartaIa)
        os.system("pause")
        os.system("cls")
        #Apartado despues de todos los calculos
        punto = ganador(carta, cartaIa, index)
        os.system("pause")
        mostrarStats(punto, listaReglas[index], rondas)
        human.borrarMazo(mazoH)
        ia.borrarMazo(mazoIa)
        if rondas["ganadas"] == 3:
            print("Ganaste la partida")
            quit()
        elif rondas["perdidas"] == 3:
            print("Perdiste la partida")
            quit()


def reqUserOpt():
    print("---------------Bienvenido---------------\n1.Iniciar Juego\n2.Salir\n")
    try:
        return int(input("\nOpción: "))
    except ValueError:
        print("Solo se admiten numeros...")


def mnuHandler():

    while(True):
        opt = reqUserOpt()
        match opt:
            case 1:
                game()
            case 2:
                print("\nSaliendo...\n")
                quit()
            case _:
                print("No se ha encontrado la opción digitada...\n")


if __name__ == "__main__":
    mnuHandler()