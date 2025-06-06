import random


def loanRequest(user):
    pass

def showData(user):
    for key, data in user.items():
        print(f"{key}, {data}")

def reqData():
    user = {
        "nombre" : "",
        "dineroSolicitado" : 0,
        "salarioAnual" : 0,
        "valorPropiedades" : 0
    }
    try:
        user["nombre"] = input("Digite el nombre del solicitante: ")
        user["dineroSolicitado"] = int(input("Cuánto dinero se está siendo solicitado? : "))
        user["salarioAnual"] = int(input("Digite el salario anual del solicitante: "))
        user["valorPropiedades"] = int(input("Digite el valor total de las propiedades del solicitante: "))
        return user;
    except:
        print("Solo se admiten números...")

def reqOptn():
    print("\nDigite 1 para solicitar el préstamo\nDigite 2 para mostrar los datos del usuario\nDigite 3 para mostrar si la solicitud fue aprobada\nDigite 4 para salir\n")
    try:
        return int(input("Opción: "))
    except ValueError:
        print("Solo se permite digitar números...")


def loanAsking():
    userOptn = 0
    while (userOptn != 4):
        userOptn = reqOptn()
        match userOptn:
            case 1:
                newUser = reqData()
            case 2:
                try:
                    showData(newUser)
                except UnboundLocalError:
                    print("\nUsuario sin registrar...")
            case 3:
                try:
                    loanRequest(newUser)
                except UnboundLocalError:
                    print("\nUsuario sin registrar...")
            case _:
                print("La opción digitada no existe...")
    print("\nSaliendo...\n")

#////////////////////////////////////////////////////////////////////////////////////////////////////////

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
            print("\n>\n")
            userTry +=1
        if (user > rndm):
            print("\n<\n")
            userTry +=1
        if (user == rndm):
            print("Felicidades has adivinado\n")
            break;
        if (userTry == 5):
            print("Lo siento, más suerte para la próxima")
    


def guessNumber():
    rndmNumber = random.randint(1,10)
    guessing(rndmNumber)


def option():
    print("digite 1 para el programa de adivinar el numero\ndigite 2 para el programa de préstamos\ndigite 3 para el programa de maquina expendedora\ndigite 4 para salir\n")
    try:
        return int(input("Opción: "));
    except ValueError:
        print("Solo se permite digitar números...")

#////////////////////////////////////////////////////////////////////////////////////////////////////////


def menuHandler():
    userOpt = 0
    while(userOpt != 4):
        userOpt = option()
        match userOpt:
            case 1:
                guessNumber()
            case 2: 
                loanAsking()
            case 3:
                pass
            case 4:
                print("Saliendo del programa...")
            case _:
                print("No se ha encontrado la opción digitada...")
            

if __name__ == "__main__":
    menuHandler()