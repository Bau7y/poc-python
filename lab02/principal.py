import tabulate
import random
import os
from colorama import Fore, Style, init
import copy


def showStats(stats, matriz):
    for key, val in stats.items():
        print(Fore.RED + f"{key}: {val}" + Style.RESET_ALL)
    print(tabulate.tabulate(matriz, tablefmt="fancy_grid"))


def calcularCamino(matriz, puntos, cordenadas, row, dire, diag):
    os.system("cls")
    print(tabulate.tabulate(matriz, tablefmt="fancy_grid"))
    pos = random.randint(0, row-1)
    print(Fore.GREEN + f"Su posición de inicio es {pos}, {0}")
    os.system("pause")
    stats = {"puntos": puntos, "cordenadas": cordenadas}
    while(stats["puntos"] < 40):
        for f in range(len(matriz)):
            for c in range(len(matriz[f])):
                pass


def llenarCamino(row, col):
    matriz = []
    for i in range(row):
        matriz.append([])
        for j in range(col):
            if j < col // 2:
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
    direcciones = [(-1,0),(1,0),(0,-1),(0,1)]
    direccionesDiag = [(-1, -1),(-1, 1),(1, -1),(1, 1)]
    row, col = solicitarNums()
    matri = llenarCamino(row, col)
    print(tabulate.tabulate(matri, tablefmt="fancy_grid"))
    os.system("pause")
    stats, matriz = calcularCamino(matri, puntos, cordenadas, row, direcciones, direccionesDiag)
    os.system("cls")
    showStats(stats, matriz)




if __name__ == "__main__":
    init()
    print(Fore.GREEN + "Bienvenido al juego Red de Caminos de Energía!" + Style.RESET_ALL)
    main()