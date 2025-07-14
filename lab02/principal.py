import tabulate
import random
import os
from colorama import Fore, Style, init

def calcularCamino(matriz, puntos, cordenadas, row):
    os.system("cls")
    print(tabulate.tabulate(matriz, tablefmt="fancy_grid"))
    pos = random.randint(0, row-1)
    for f in range(len(matriz)):
        for c in range(len(matriz[f])):
            print(f"Actualmente se encuentra en la posición {pos},{0}")


def llenarCamino(row, col):
    matriz = []
    for i in range(row):
        matriz.append([])
        for j in range(col):
            if j < col//2:
                matriz[i].append(random.randint(1, 15))
            else:
                if j < int(col*0.75):
                    matriz[i].append(-random.randint(1, 15))
                else:
                    matriz[i].append(random.randint(1, 15))
    return matriz


def  solicitarNums():
    try:
        return int(input("Ingrese la cantidad de filas que desea para la matriz: ")), int(input("Ingrese la cantidad de columnas que desea para la matriz: "))
    except ValueError:
        print(Fore.RED + "Error: Ingrese un número válido." + Style.RESET_ALL)
        return solicitarNums()

def main():
    puntos = 100
    cordenadas = []
    row, col = solicitarNums()
    matri = llenarCamino(row, col)
    print(tabulate.tabulate(matri, tablefmt="fancy_grid"))
    os.system("pause")
    stats = calcularCamino(matri, puntos, cordenadas, row)




if __name__ == "__main__":
    init()
    print(Fore.GREEN + "Bienvenido al juego Red de Caminos de Energía!" + Style.RESET_ALL)
    main()