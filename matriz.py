import random
import tabulate

def condicion(matriz,col,row):
    if matriz[col][row] % 2 == 0:
        matriz[col][row] = "$"
    else:
        matriz[col][row] = "#"
    return matriz

def matriz5():
    matriz = []
    for col in range(0, 5):
        matriz.append([])
        for row in range(0, 5):
            matriz[col].append(random.randint(0, 50))
            matriz = condicion(matriz, col, row)
    print(tabulate.tabulate(matriz, tablefmt="grid"))

def matriz():
    matriz = []
    for col in range(0, 5):
        matriz.append([])
        for row in range(0, 5):
            matriz[col].append(0)
    return matriz



if __name__ == "__main__":
    matriz1 = matriz()
    matriz5x5 = matriz5()