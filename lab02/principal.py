import tabulate
import random
import os
from colorama import Fore, Style, init


def primo(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True


def showStats(stats, matriz):
    for key, val in stats.items():
        print(Fore.RED + f"{key}: {val}" + Style.RESET_ALL)
    print(tabulate.tabulate(matriz, tablefmt="fancy_grid"))


def calcularCamino(matriz, row, dire):
    os.system("cls")
    print(tabulate.tabulate(matriz, tablefmt="fancy_grid"))
    os.system("pause")
    stats = {"puntos": 100, "cordenadas": []}
    actFila = random.randint(0, row - 1)
    print(Fore.GREEN + f"Su posición de inicio es {actFila}, {0}")
    actCol = 0
    while True:
        numActual = matriz[actFila][actCol]
        if stats["cordenadas"] == []:
            if matriz[actFila][actCol] > 10:
                actFila = random.randint(0, row - 1)
        valorMax = numActual
        nuevaPos = (actFila, actCol)
        encontrado = False

        for dx, dy in dire:
            nuevFila = actFila + dx
            nuevCol = actCol + dy

            if 0 <= nuevFila < len(matriz) and 0 <= nuevCol < len(matriz[0]):
                vecino = matriz[nuevFila][nuevCol]
                if abs(vecino) > abs(valorMax) and primo(abs(vecino) + abs(valorMax)):
                    valorMax = vecino
                    nuevaPos = (nuevFila, nuevCol)
                    encontrado = True
                    if vecino < 0:
                        stats["puntos"] -= 3
                    elif (nuevFila - actFila) == 1 and (nuevCol - actCol) == 1:
                        stats["puntos"] -= 2
                    else:
                        stats["puntos"] -= 1

        if not encontrado:
            break
        actFila, actCol = nuevaPos
        stats["cordenadas"].append(nuevaPos)
    return stats, matriz


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
    direcciones = [(0,1),(-1,1),(1,1),(-1,0),(1,0)]
    row, col = solicitarNums()
    matri = llenarCamino(row, col)
    print(tabulate.tabulate(matri, tablefmt="fancy_grid"))
    os.system("pause")
    stats, matriz = calcularCamino(matri, row, direcciones)
    showStats(stats, matriz)




if __name__ == "__main__":
    init()
    print(Fore.GREEN + "Bienvenido al juego Red de Caminos de Energía!" + Style.RESET_ALL)
    main()