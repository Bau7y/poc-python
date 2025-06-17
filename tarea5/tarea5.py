def reqUserOpt():
    print("1.Reporte\n2.Personas\n3.Divisas\n4.Salir\n")
    try:
        return int(input("Opción: "))
    except ValueError:
        print("Debe digitar una de las opciones...")


def menuHandler():
    while(True):
        userOpt = reqUserOpt()
        match userOpt:
            case 1:
                print("Reporte")
            case 2:
                print("Personas")
            case 3:
                print("Divisas")
            case 4:
                print("Saliendo...")
                quit()
            case _:
                print("No se ha encontrado la opción digitada...")

if __name__ == "__main__":
    menuHandler()