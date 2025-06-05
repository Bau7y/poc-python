def option():
    print("digite 1 para el programa de adivinar el numero")


def menuHandler():
    userOpt = 0
    while(userOpt != 4):
        userOpt = option()
        match userOpt:
            case 1:
                pass
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