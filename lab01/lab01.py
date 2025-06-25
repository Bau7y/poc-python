import random, os
from Humano import Humano

def reqCard(mazo):
    while(True):
        try:
            option = input("\nSeleccione una carta(# de ????): ")
            for key, val in mazo.items():
                if option == key:
                    selectedCard = [key, val]
                    print("\nCarta seleccionada: ", selectedCard)
                    return selectedCard
            print("\nNo se ha encontrado la carta solicitada\n")
        except:
            print("Solo se admiten numeros...")


def showCards(mazo):
    carta=0
    while(carta < 5):
        for key, value in mazo.items():
            carta +=1
            print(f"{carta}. ",key, value)


def game():
    ronda = 0
    while(ronda < 5):
        listaReglas = ["conocimiento + estrategia", "estrategia + energía", "(conocimiento * 2) - energía", "conocimiento + estrategia + energía", "estrategia * energía"]
        index = random.randint(0,4)
        mazo = Humano().getCartas()
        os.system("cls")
        print("---------------Humano vs IA---------------\nRegla de la ronda: ", listaReglas[index], "\n\n")
        showCards(mazo)
        card = reqCard(mazo)
        os.system("pause")
        ronda += 1

def reqUserOpt():
    print("---------------Bienvenido---------------\n1.Iniciar Juego\n2.Salir")
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