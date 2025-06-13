
def reqUserOpt():
    print("1. Registro de personas y esquema de vacunación\n2. Reportes\n3. Salir\n")
    try:
        return int(input("Opción: "))
    except ValueError:
        print("Solo se permiten numeros enteros...")


def menuHandler():
    while(True):
        userOpt = reqUserOpt()
        match userOpt:
            case 1:
                pass
            case 2:
                pass
            case 3:
                print("Saliendo...")
                quit()
            case _:
                print("No se ha encontrado la opción digitada...\n")

if __name__ == "__main__":
    menuHandler()