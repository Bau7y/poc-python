import random

def generarListaNums():
    listaNums = []
    for i in range(0, 20):
        listaNums.append(random.randint(1, 500))
    print(listaNums)
    listaNums.sort()
    print(listaNums[0], " Es el menor, y el mayor es ", listaNums[-1])


def showLists(listaMen, listaMay):
    print("Lista de numeros menores o iguales a 50: ", listaMen, "\n Contiene: ", len(listaMen), " numeros")
    print("Lista de numeros mayores a 50: ", listaMay, "\n Contiene: ", len(listaMay), " numeros")

def generarListas(lista):
    listaMenores = [ num for num in lista if num <= 50 ]
    listaMayores = [ num for num in lista if num > 50 ]
    listaMenores.sort()
    listaMayores.sort()
    return listaMenores, listaMayores;

def crearLista():
    lista = []
    for i in range(0, 20):
        lista.append(random.randint(0, 100))
    print(lista)
    return lista;

def reqUserOption():
    print("1.Generar Listas\n2.Mostrar Listas\n3.Numeros\n4.Salir")
    try:
        return int(input("Digite una opcion: "))
    except:
        print("Solo se permiten numeros...")

def menuHandler():
    userOption = 0
    while (True):
        userOption = reqUserOption()
        match userOption:
            case 1:
                newList = crearLista()
                listaMen, listaMay = generarListas(newList)
            case 2:
                try:
                    showLists(listaMen, listaMay)
                except UnboundLocalError:
                    print("Lista no generada...")
            case 3:
                generarListaNums()
            case 4:
                print("Saliendo...")
                quit()
            case _:
                print("No se ha encontrado la opción digitada...")

if __name__ == "__main__":
    menuHandler()