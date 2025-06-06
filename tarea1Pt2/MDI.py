import random

 #///////////////////////////////////////////Programa Adivinar el numero/////////////////////////////////
def reqNumber():
    try:
        return int(input("Digite su numero: "))
    except ValueError:
        print("Solo se admiten numeros")


def guessing(rndm):
    userTry = 0
    while(userTry < 5):
        user = reqNumber()
        if (user < rndm):
            print(">")
            userTry +=1
        if (user > rndm):
            print("<")
            userTry +=1
        if (user == rndm):
            print("Felicidades has adivinado")
            break;
        if (userTry == 5):
            print("Lo siento, más suerte para la próxima")
    


def guessNumber():
    rndmNumber = random.randint(1,10)
    guessing(rndmNumber)


def option():
    print("digite 1 para el programa de adivinar el numero\ndigite 2 para el programa de préstamos\ndigite 3 para el programa de maquina expendedora\ndigite 4 para salir")
    try:
        return int(input("Opción: "));
    except ValueError:
        print("Solo se permite digitar números...")

#////////////////////////////////////////////////////////////////////////////////////////////////////////////


def menuHandler():
    userOpt = 0
    while(userOpt != 4):
        userOpt = option()
        match userOpt:
            case 1:
                guessNumber()
            case 2: 
                pass
            case 3:
                pass
            case 4:
                print("Saliendo del programa...")
            case _:
                print("No se ha encontrado la opción digitada...")
            

if __name__ == "__main__":
    menuHandler()