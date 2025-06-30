import os
import random
import tabulate

def mostrarLista(listaCordenadas):
    if listaCordenadas == []:
        print("El valor no se encuentra en la matriz")
        return
    print(f"se encuentra en la posición: {listaCordenadas}")

def encontrar_valor(matriz, valor):
    print("valor a buscar: ", valor)
    listaCordenadas = []
    for row in range(len(matriz)):
        for col in range(len(matriz[row])):
            if matriz[row][col] == valor:
                listaCordenadas.append([row, col])
    return listaCordenadas


def matriz5x6():
    matriz = []
    for row in range(5):
        matriz.append([])
        for col in range(6):
            matriz[row].append(random.randint(1, 20))
    print(tabulate.tabulate(matriz, tablefmt="grid"))
    listaCordenadas = encontrar_valor(matriz, random.randint(1, 20))
    mostrarLista(listaCordenadas)

def condicion(matri, row):
    contador = 0
    for row in range(len(matri)-1):
        if matri[row][0] == 5:
            contador += 1
    return contador

    
def matriz():
    os.system("cls")
    matri = []
    filas = int(input("Digite la cantidad de filas para hacer la matriz: "))
    columnas = int(input("Digite la cantidad de columnas para hacer la matriz: "))
    for row in range(0, filas):
        matri.append([])
        for col in range(0, columnas):
            matri[row].append(random.randint(1, 20))
            contador = condicion(matri, row)
    os.system("cls")
    print(tabulate.tabulate(matri, tablefmt="grid"))
    print(f"\nLa cantidad de veces que se repite el 5 en el inicio de las filas es: {contador}\n")
    


def reqUserOpt():
    print("1. Cantidad de Filas\n2. Encontrar Valor\n3.Salir\n\n")
    try:
        return int(input("Opción: "))
    except ValueError:
        print("Solo se permiten numeros enteros...")



def mnuHandler():
    while(True):
        userOpt = reqUserOpt()
        match userOpt:
            case 1:
                matriz()
            case 2:
                matriz5x6()
            case 3:
                print("Saliendo...")
                quit()
            case _:
                print("No se ha encontrado la opción digitada...\n")



if __name__ == "__main__":
    mnuHandler()