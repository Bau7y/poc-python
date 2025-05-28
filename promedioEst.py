def calcProm(notas):
    for index in notas:
        nota = index+index+index
    return nota/3
        

def reqProms():
    listaNotas = []
    for i in range(0, 3):
        user = int(input("Digite las tres notas del estudiante: "))
        listaNotas.append(user)
    return listaNotas


def main():
    listaNotas = reqProms()
    promEst = calcProm(listaNotas)
    print("El promedio del estudiante es de ", promEst )


if __name__ == '__main__':
    main()