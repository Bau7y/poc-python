import random, os
from Humano import Humano

def showCards():
    mazo = Humano().getCartas()
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
        os.system("cls")
        print("---------------Juego---------------\nRegla de la ronda: ", listaReglas[index], "\n\n")
        showCards()
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