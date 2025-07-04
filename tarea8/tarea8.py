
def reqUserOpt():
    print("1. Generar Matriz de temperaturas\n2. Ver resultados\n3. Salir")
    try:
        return int(input("\nIngrese una opcion: "))
    except ValueError:
        print("Solo se admiten números...")
    


def mnuHandler():
    matrizGrados = []
    while(True):
        userOpt = reqUserOpt()
        match userOpt:
            case 1:
                pass
            case 2:
                pass
            case 3:
                print("saliendo...")
                quit()
            case _:
                print("Opcion invalida")


if __name__ == "__main__":
    mnuHandler()