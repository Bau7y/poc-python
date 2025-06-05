def option():
    print("digite 1 para el programa de adivinar el numero")
    print("digite 2 para el programa de préstamos")
    print("digite 3 para el programa de maquina expendedora")
    print("digite 4 para salir...")
    try:
        return int(input("Opción: "));
    except ValueError:
        print("Solo se permite digitar números...")


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