import random
import tabulate

def mostrarAltaBajaTemp(matriz, lista):
    for row in range(len(matriz)):
        for col in range(len(matriz[row])):
            if matriz[row][col] == max(lista):
                print(f"\nLa temperatura mas alta del mes es en la semana {row+1} con: {matriz[row][col]} grados, en el día {listaDias[col]}")
            if matriz[row][col] == min(lista):
                print(f"\nLa temperatura mas baja del mes es en la semana {row+1} con: {matriz[row][col]} grados, en el día {listaDias[col]}\n")


def mostrarAltaBajaMes(matriz):
    listaTemperaturas = []
    for row in range(len(matriz)):
        for col in range(len(matriz[row])):
            listaTemperaturas.append(matriz[row][col])
    mostrarAltaBajaTemp(matriz, listaTemperaturas)


def mostrarPromedio(matriz):
    for row in range(len(matriz)):
        print(f"El promedio de la semana {row+1} es: {sum(matriz[row])//len(matriz[row])} grados\n")


def mostrarAltaBajaSem(matriz):
    for row in range(len(matriz)):
        for col in range(len(matriz[row])):
            if matriz[row][col] == max(matriz[row]):
                print(f"La temperatura mas alta de la semana {row+1} es: {matriz[row][col]} grados, en el día {listaDias[col]}")
            if matriz[row][col] == min(matriz[row]):
                print(f"La temperatura mas baja de la semana {row+1} es: {matriz[row][col]} grados, en el día {listaDias[col]}\n")
            


def reqNewUserOpt():
    print("1. Mostrar la temperatura más alta y más baja\n2. Mostrar el promedio de temperatura de cada una de las semanas\n3. Mostrar la temperatura más alta de todo el mes\n4. Salir")
    try:
        return int(input("\nIngrese una opcion: "))
    except ValueError:
        print("Solo se admiten números...")


def showData(matriz):
    while(True):
        newUserOpt = reqNewUserOpt()
        match newUserOpt:
            case 1:
                mostrarAltaBajaSem(matriz)
            case 2:
                mostrarPromedio(matriz)
            case 3:
                mostrarAltaBajaMes(matriz)
            case 4:
                print("saliendo...")
                break
            case _:
                print("Opcion invalida")


def llenarMatriz():
    matriz = []
    for row in range(4):
        matriz.append([])
        for col in range(7):
            matriz[row].append(random.randint(7, 38))
    return matriz


def reqUserOpt():
    print("1. Generar Matriz de temperaturas\n2. Ver resultados\n3. Salir")
    try:
        return int(input("\nIngrese una opcion: "))
    except ValueError:
        print("Solo se admiten números...")
    


def mnuHandler():
    while(True):
        userOpt = reqUserOpt()
        match userOpt:
            case 1:
                matrizGrados = llenarMatriz()
                print(tabulate.tabulate(matrizGrados, tablefmt="fancy_grid"))
            case 2:
                try: 
                    showData(matrizGrados)
                except UnboundLocalError:
                    print("\nNo hay datos registrados...\n")
            case 3:
                print("saliendo...")
                quit()
            case _:
                print("Opcion invalida")


if __name__ == "__main__":
    listaDias = ["Domingo", "Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado"]
    mnuHandler()
    