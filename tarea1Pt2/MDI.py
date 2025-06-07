import random

def showRes(change, amount, diff):
    print(f"\nVuelto: {diff}\n")
    for coin, amount in change.items():
        print(f"{amount} moneda(s) de {coin}\n")


def calcChange(prodVal, customerPay):
    if (prodVal > customerPay):
        print("Lo sentimos...El costo del producto es mayor al monto ingresado\n")
    else:
        difference = customerPay - prodVal
        shDiff = difference
        coinList = [100, 50, 25, 5, 1]
        change = {}
        for value in coinList:
            amount = difference // value
            if amount > 0:
                change[value] = amount
                difference %= value
        showRes(change, amount, shDiff)


def reqProdCost():
    try:
        return int(input("Digite el costo del articulo: "));
    except ValueError:
        print("Solo se admiten numeros...")

def reqMoney():
    try:
        return int(input("Digite el monto con el que va a pagar el articulo: "));
    except ValueError:
        print("Solo se admiten numeros...")


def vendingMachine():
    productVal = reqProdCost()
    customer = reqMoney()
    calcChange(productVal, customer)

 #///////////////////////////////////////////Programa solicitud de prestamo/////////////////////////////////
def loanRequest(user):
    userPoints = 0;
    if (user["salarioAnual"] >= user["dineroSolicitado"] * 0.50):
        userPoints += 5;
    if ((user["salarioAnual"] >= user["dineroSolicitado"] * 0.25) and (user["salarioAnual"] <= user["dineroSolicitado"] * 0.50)):
        userPoints += 3;
    if ((user["salarioAnual"] >= user["dineroSolicitado"] * 0.10) and (user["salarioAnual"] < user["dineroSolicitado"] * 0.25)):
        userPoints += 1;
    if (user["dineroSolicitado"] * 2 >= user["valorPropiedades"]):
        userPoints += 5;
    if (user["dineroSolicitado"] == user["valorPropiedades"]):
        userPoints += 3;
    if (userPoints >= 6):
        print(f"Préstamo aceptado!!!\n{user["nombre"]}, usted cuenta con un total de: {userPoints}", " Puntos")
    else:
        print("Rechazado...\nPuntos: ", userPoints)


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
                vendingMachine()
            case 4:
                print("Saliendo del programa...")
            case _:
                print("No se ha encontrado la opción digitada...")
            

if __name__ == "__main__":
    menuHandler()